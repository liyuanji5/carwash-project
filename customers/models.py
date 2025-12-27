from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    DISCOUNT_CHOICES = [
        (0, "Без скидки"),
        (5, "5%"),
        (10, "10%"),
        (15, "15%"),
        (20, "20%"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="customer_profile",
    )
    phone = models.CharField("Телефон", max_length=20)
    car_model = models.CharField("Марка автомобиля", max_length=100, blank=True)
    car_number = models.CharField("Госномер", max_length=20, blank=True)
    discount = models.PositiveIntegerField(
        "Скидка (%)", choices=DISCOUNT_CHOICES, default=0
    )
    notes = models.TextField("Заметки", blank=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.phone}"
