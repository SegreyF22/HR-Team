from rest_framework import viewsets, filters
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['last_name', 'first_name', 'patronymic']
    filters_fields = ['department']


