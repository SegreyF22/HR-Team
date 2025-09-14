from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DepartmentViewSet, UserViewSet, SalaryAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees/<int:pk>/salary/', SalaryAPIView.as_view(), name='employee-salary' )
]