from django.contrib import admin
from .models import Employee, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'employees_count')
    readonly_fields = ('employees_count',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'position',
                    'department', 'date_hired', 'tenure_display')
    list_filter = ('department',)
    search_fields = ('last_name', 'first_name', 'patronymic')