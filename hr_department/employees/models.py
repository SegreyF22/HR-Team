from datetime import date

from django.db import models
from django.utils import timezone
import secrets
import string
from unidecode import unidecode


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название отдела')
    specialization = models.TextField(blank=True, verbose_name='Специфика работы')
    employees_count = models.PositiveIntegerField(default=0, verbose_name='Количество сотрудников')

    class Meta:
        db_table = 'departments'
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name

    def calculate_employees_count(self):
        count = self.employees.count()
        self.employees_count = count
        self.save(update_fields=["employees_count"])
        return count


class Employee(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,
                                   blank=True, related_name='employees', verbose_name='Отдел')
    position = models.CharField(max_length=200, blank=True, verbose_name='Должность')
    rank = models.CharField(max_length=100, default='Рядовой', verbose_name='Звание')
    date_hired = models.DateField(verbose_name='Дата приема на работу')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        fio = ' '.join(filter(None, [self.last_name, self.first_name, self.patronymic]))
        return fio

    def get_tenure(self, as_of: date = None):
        """Возвращает стаж работы"""
        if not as_of:
            as_of = timezone.localdate()

        start = self.date_hired
        end = as_of
        if end < start:
            return 0, 0, 0

        years = end.year - start.year
        months = end.month - 1 or 12
        days = end.day - start.day

        if days < 0:
            from calendar import monthrange
            prev_month = end.month - 1 or 12
            prev_year = end.year if end.month != 1 else end.year - 1
            days_in_prev = monthrange(prev_year, prev_month)[1]
            days += days_in_prev
            months -= 1

        if months < 0:
            months += 12
            years -= 1

        return years, months, days

    @property
    def tenure_display(self):
        y, m, d = self.get_tenure()

        parts = []
        if y:
            parts.append(
                f"{y} {'год' if y % 10 == 1 and y % 100 != 11 else 'года' if 2 <= y % 10 <= 4 and not 12 <= y % 100 <= 14 else 'лет'}")
        if m:
            parts.append(
                f"{m} {'месяц' if m % 10 == 1 and m % 100 != 11 else 'месяца' if 2 <= m % 10 <= 4 and not 12 <= m % 100 <= 14 else 'месяцев'}")
        if d:
            parts.append(
                f"{d} {'день' if d % 10 == 1 and d % 100 != 11 else 'дня' if 2 <= d % 10 <= 4 and not 12 <= d % 100 <= 14 else 'дней'}")
        return ', '.join(parts) if parts else '0 дней'

class User(models.Model):
    user_id = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='user', verbose_name='Сотрудник')
    name = models.CharField(max_length=255, editable=False, verbose_name='Имя пользователя')
    login = models.CharField(max_length=255, unique=True, editable=False, verbose_name='Логин')
    password = models.CharField(max_length=100, editable=False, verbose_name='Пароль')

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.name:
            initials = ''
            if self.user_id.last_name:
                initials += self.user_id.last_name[0]
            if self.user_id.patronymic:
                initials += self.user_id.patronymic[0]
            self.name = f"{self.user_id.first_name}{initials}".strip()

        if not self.login:
            self.login = unidecode(self.name.lower().replace(' ', ''))

        if not self.password:
            alphabet = string.ascii_letters + string.digits
            self.password = ''.join(secrets.choice(alphabet) for _ in range(10))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.login



