from django.contrib import admin
from .models import Employee, Department, User

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'employees_count')
    readonly_fields = ('employees_count',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'patronymic', 'position',
                    'department', 'date_hired', 'tenure_display')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name', 'patronymic')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'login', 'password')
    readonly_fields = ('name', 'login', 'password')

