from rest_framework import serializers

from .models import Employee, Department, User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'specialization', 'employees_count']


class EmployeeSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()
    tenure = serializers.SerializerMethodField()
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',
                                                       write_only=True, required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'fio', 'position', 'rank', 'department',
                  'department_id', 'date_hired', 'date_of_birth', 'tenure']

    def get_fio(self, obj):
        return str(obj)

    def get_tenure(self, obj):
        years, months, days = obj.get_tenure()
        return {'years': years, 'months': months, 'days': days, 'display': obj.tenure_display}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'login', 'password']
        read_only_fields = ['name', 'login', 'password']
