from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee, User

@receiver([post_save, post_delete], sender=Employee)
def update_department_employees_count(sender, instance, **kwargs):
    if instance.department:
        instance.department.calculate_employees_count()

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'user'):
        User.objects.create(user_id=instance)