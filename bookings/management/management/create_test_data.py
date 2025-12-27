from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ServiceCategory, Service
from customers.models import Customer
from employees.models import Position, Employee
from bookings.models import Box
from datetime import date


class Command(BaseCommand):
    help = "Создание тестовых данных для автомойки"

    def handle(self, *args, **options):
        # Создаем категории услуг
        categories = [
            ("Мойка кузова", "Наружная мойка автомобиля", 1),
            ("Чистка салона", "Внутренняя уборка", 2),
            ("Полировка", "Полировка кузова", 3),
            ("Дополнительные услуги", "Прочие услуги", 4),
        ]

        for name, description, order in categories:
            ServiceCategory.objects.get_or_create(
                name=name, defaults={"description": description, "order": order}
            )

        # Создаем услуги
        services = [
            ("Экспресс-мойка", "Быстрая мойка", 500, 15, 1),
            ("Стандартная мойка", "Полная мойка", 1000, 30, 1),
            ("Комплексная мойка", "Мойка + сушка", 1500, 45, 1),
            ("Чистка салона", "Вакуумная чистка", 800, 40, 2),
            ("Химчистка салона", "Глубокая чистка", 2500, 120, 2),
        ]

        for name, description, price, duration, category_id in services:
            Service.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "duration": duration,
                    "category_id": category_id,
                },
            )

        # Создаем боксы
        for i in range(1, 5):
            Box.objects.get_or_create(
                number=i,
                defaults={
                    "box_type": "standard" if i <= 2 else "premium",
                    "capacity": 2,
                },
            )

        # Создаем должности
        positions = ["Мойщик", "Администратор", "Менеджер"]
        for position_name in positions:
            Position.objects.get_or_create(name=position_name)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
