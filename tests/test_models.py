from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, time
from services.models import ServiceCategory, Service
from customers.models import Customer
from employees.models import Position, Employee
from bookings.models import Box, Booking


class ServiceModelTest(TestCase):
    """Тесты для моделей услуг"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Мойка кузова", description="Наружная мойка автомобиля", order=1
        )

        self.service = Service.objects.create(
            name="Комплексная мойка",
            description="Полная мойка автомобиля",
            price=1500,
            duration=60,
            category=self.category,
            is_active=True,
        )

    def test_service_creation(self):
        """Тест создания услуги"""
        self.assertEqual(self.service.name, "Комплексная мойка")
        self.assertEqual(self.service.price, 1500)
        self.assertEqual(self.service.duration, 60)
        self.assertTrue(self.service.is_active)
        self.assertEqual(str(self.service), "Комплексная мойка - 1500 руб.")

    def test_service_category_creation(self):
        """Тест создания категории услуг"""
        self.assertEqual(self.category.name, "Мойка кузова")
        self.assertEqual(self.category.order, 1)
        self.assertEqual(str(self.category), "Мойка кузова")


class CustomerModelTest(TestCase):
    """Тесты для модели клиента"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testcustomer", email="customer@test.com", password="testpass123"
        )

        self.customer = Customer.objects.create(
            user=self.user,
            phone="+79123456789",
            car_model="Toyota Camry",
            car_number="А123АА777",
            discount=10,
            notes="Постоянный клиент",
        )

    def test_customer_creation(self):
        """Тест создания клиента"""
        self.assertEqual(self.customer.phone, "+79123456789")
        self.assertEqual(self.customer.car_model, "Toyota Camry")
        self.assertEqual(self.customer.car_number, "А123АА777")
        self.assertEqual(self.customer.discount, 10)
        self.assertEqual(self.customer.notes, "Постоянный клиент")
        self.assertEqual(str(self.customer), "testcustomer - +79123456789")

    def test_customer_discount_choices(self):
        """Тест доступных значений скидки"""
        valid_discounts = [0, 5, 10, 15, 20]
        for discount in valid_discounts:
            customer = Customer.objects.create(
                user=User.objects.create_user(
                    username=f"test{discount}", password="testpass123"
                ),
                phone=f"+791200000{discount}",
                discount=discount,
            )
            self.assertIn(customer.discount, valid_discounts)


class EmployeeModelTest(TestCase):
    """Тесты для модели сотрудника"""

    def setUp(self):
        self.position = Position.objects.create(
            name="Мойщик", description="Мойка автомобилей"
        )

        self.user = User.objects.create_user(
            username="testemployee", email="employee@test.com", password="testpass123"
        )

        self.employee = Employee.objects.create(
            user=self.user,
            position=self.position,
            phone="+79123456780",
            hire_date=date(2024, 1, 1),
            is_active=True,
        )

    def test_employee_creation(self):
        """Тест создания сотрудника"""
        self.assertEqual(self.employee.phone, "+79123456780")
        self.assertEqual(self.employee.hire_date, date(2024, 1, 1))
        self.assertTrue(self.employee.is_active)
        self.assertEqual(str(self.employee), "testemployee - Мойщик")

    def test_position_creation(self):
        """Тест создания должности"""
        self.assertEqual(self.position.name, "Мойщик")
        self.assertEqual(str(self.position), "Мойщик")


class BoxModelTest(TestCase):
    """Тесты для модели бокса"""

    def setUp(self):
        self.box = Box.objects.create(
            number=1, box_type="standard", capacity=2, is_active=True
        )

    def test_box_creation(self):
        """Тест создания бокса"""
        self.assertEqual(self.box.number, 1)
        self.assertEqual(self.box.box_type, "standard")
        self.assertEqual(self.box.capacity, 2)
        self.assertTrue(self.box.is_active)
        self.assertEqual(str(self.box), "Бокс 1 (Стандартный)")

    def test_box_type_choices(self):
        """Тест доступных типов боксов"""
        box_premium = Box.objects.create(number=2, box_type="premium", capacity=2)
        self.assertEqual(box_premium.box_type, "premium")
        self.assertEqual(box_premium.get_box_type_display(), "Премиум")


class BookingModelTest(TestCase):
    """Тесты для модели бронирования"""

    def setUp(self):
        # Создаем пользователя и клиента
        self.user = User.objects.create_user(
            username="bookinguser", password="testpass123"
        )
        self.customer = Customer.objects.create(user=self.user, phone="+79123456789")

        # Создаем категорию и услугу
        self.category = ServiceCategory.objects.create(name="Мойка")
        self.service = Service.objects.create(
            name="Стандартная мойка", price=1000, duration=30, category=self.category
        )

        # Создаем бокс
        self.box = Box.objects.create(number=1, box_type="standard", capacity=2)

        # Создаем бронирование
        self.booking = Booking.objects.create(
            customer=self.customer,
            service=self.service,
            box=self.box,
            booking_date=date(2024, 1, 15),
            booking_time=time(10, 0),
            status="pending",
        )

    def test_booking_creation(self):
        """Тест создания бронирования"""
        self.assertEqual(self.booking.service.name, "Стандартная мойка")
        self.assertEqual(self.booking.booking_date, date(2024, 1, 15))
        self.assertEqual(self.booking.booking_time, time(10, 0))
        self.assertEqual(self.booking.status, "pending")
        self.assertEqual(self.booking.total_price, 1000)  # Без скидки
        self.assertEqual(
            str(self.booking), "bookinguser - Стандартная мойка - 2024-01-15"
        )

    def test_booking_with_discount(self):
        """Тест расчета цены со скидкой"""
        # Создаем клиента со скидкой
        discount_user = User.objects.create_user(
            username="discountuser", password="testpass123"
        )
        discount_customer = Customer.objects.create(
            user=discount_user, phone="+79123456780", discount=20  # 20% скидка
        )

        booking_with_discount = Booking.objects.create(
            customer=discount_customer,
            service=self.service,
            box=self.box,
            booking_date=date(2024, 1, 16),
            booking_time=time(11, 0),
            status="pending",
        )

        # Проверяем расчет цены со скидкой
        expected_price = 1000 * 0.8  # 20% скидка = 800 руб.
        self.assertEqual(booking_with_discount.total_price, expected_price)

    def test_booking_status_choices(self):
        """Тест доступных статусов бронирования"""
        statuses = ["pending", "confirmed", "in_progress", "completed", "cancelled"]

        for status in statuses:
            booking = Booking.objects.create(
                customer=self.customer,
                service=self.service,
                box=self.box,
                booking_date=date(2024, 1, 17),
                booking_time=time(12, 0),
                status=status,
            )
            self.assertIn(booking.status, statuses)

    def test_booking_save_method(self):
        """Тест метода save с перерасчетом цены"""
        # Меняем скидку у клиента
        self.customer.discount = 10
        self.customer.save()

        # Обновляем бронирование
        self.booking.save()

        # Проверяем, что цена пересчиталась
        expected_price = 1000 * 0.9  # 10% скидка = 900 руб.
        self.assertEqual(self.booking.total_price, expected_price)
