from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from customers.models import Customer
from employees.models import Employee


class Box(models.Model):
    BOX_TYPES = [
        ("standard", "Стандартный"),
        ("premium", "Премиум"),
    ]

    number = models.PositiveIntegerField("Номер бокса", unique=True)
    box_type = models.CharField("Тип бокса", max_length=20, choices=BOX_TYPES)
    capacity = models.PositiveIntegerField("Вместимость (машин)", default=2)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f"Бокс {self.number} ({self.get_box_type_display()})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтвержден"),
        ("in_progress", "В процессе"),
        ("completed", "Завершен"),
        ("cancelled", "Отменен"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="bookings",
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name="Услуга"
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мойщик",
    )
    box = models.ForeignKey(
        Box, on_delete=models.SET_NULL, null=True, verbose_name="Бокс"
    )
    booking_date = models.DateField("Дата бронирования")
    booking_time = models.TimeField("Время бронирования")
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    total_price = models.DecimalField(
        "Итоговая цена", max_digits=8, decimal_places=2, editable=False
    )
    notes = models.TextField("Заметки", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-booking_date", "-booking_time"]

    def save(self, *args, **kwargs):
        # Расчет цены со скидкой
        discount_amount = (self.service.price * self.customer.discount) / 100
        self.total_price = self.service.price - discount_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.customer.user.username} - {self.service.name} - {self.booking_date}"
        )
