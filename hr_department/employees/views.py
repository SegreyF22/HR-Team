from rest_framework import viewsets, filters, status
from .models import Employee, Department, User
from .serializers import EmployeeSerializer, DepartmentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

import os
import requests

ACCOUNTING_URL = os.getenv('ACCOUNTING_URL', 'http://localhost:8001')

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['last_name', 'first_name', 'patronymic']
    filters_fields = ['department']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('user_id').all()
    serializer_class = UserSerializer

class SalaryAPIView(APIView):
    """
    GET /api/employees/{id}/salary/
       Обращается к accounting сервису и возвращает расчёт зарплаты.
    """
    def get(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not fount"}, status=status.HTTP_404_NOT_FOUND)

        # определяем стаж в полных годах(используем get_tenure)
        years, months, days = employee.get_tenure()
        tenure_years = years
        # вызываем бухгалтерию
        try:
            resp = requests.get(f"{ACCOUNTING_URL}/salary/{employee.id}", params={"years": tenure_years}, timeout=5)
        except requests.RequestException as e:
            return Response({"detail": "Failed to reach accounting service", "error": str(e)},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if resp.status_code != 200:
            return Response({"detail": "Accounting service error", "status_code": resp.status_code,
                             "response": resp.text}, status=status.HTTP_502_BAD_GATEWAY)

        data = resp.json()
        result = {
            "employee": {
                "id": employee.id,
                "fio": str(employee),
                "position": employee.position,
                "department": employee.department.name if employee.department else None,
                "date_hired": employee.date_hired.isoformat(),
            },
            "salary": data
        }
        return Response(result, status=status.HTTP_200_OK)




