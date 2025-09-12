from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DepartmentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls