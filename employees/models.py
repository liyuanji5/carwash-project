from django.db import models
from django.contrib.auth.models import User


class Position(models.Model):
    name = models.CharField("Название должности", max_length=100)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="employee_profile",
    )
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, verbose_name="Должность"
    )
    phone = models.CharField("Телефон", max_length=20)
    hire_date = models.DateField("Дата приема на работу")
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.position}"
