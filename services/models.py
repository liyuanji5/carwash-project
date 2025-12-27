from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField("Название категории", max_length=200)
    description = models.TextField("Описание", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField(
        "Длительность (мин)", help_text="Продолжительность в минутах"
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="services",
    )
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "Услуги"
        ordering = ["category__order", "name"]

    def __str__(self):
        return f"{self.name} - {self.price} руб."
