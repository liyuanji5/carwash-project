from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from bookings.forms import UserRegistrationForm, BookingForm
from customers.forms import CustomerUpdateForm
from services.models import ServiceCategory, Service
from customers.models import Customer


class UserRegistrationFormTest(TestCase):
    """Тесты для формы регистрации пользователя"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Мойка")
        self.service = Service.objects.create(
            name="Тестовая услуга", price=1000, duration=30, category=self.category
        )

    def test_valid_registration_form(self):
        """Тест валидной формы регистрации"""
        form_data = {
            "username": "newuser",
            "email": "new@test.com",
            "first_name": "Иван",
            "last_name": "Иванов",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "phone": "+79123456789",
            "car_model": "Toyota",
            "car_number": "А123АА777",
        }

        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_save(self):
        """Тест сохранения формы регистрации"""
        form_data = {
            "username": "newuser",
            "email": "new@test.com",
            "first_name": "Иван",
            "last_name": "Иванов",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "phone": "+79123456789",
        }

        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Проверяем, что пользователь создан
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@test.com")

        # Проверяем, что профиль клиента создан
        self.assertTrue(hasattr(user, "customer_profile"))
        self.assertEqual(user.customer_profile.phone, "+79123456789")

    def test_invalid_registration_form(self):
        """Тест невалидной формы регистрации"""
        # Пароли не совпадают
        form_data = {
            "username": "newuser",
            "email": "new@test.com",
            "password1": "password123",
            "password2": "differentpassword",
            "phone": "+79123456789",
        }

        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class BookingFormTest(TestCase):
    """Тесты для формы бронирования"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Мойка")
        self.service = Service.objects.create(
            name="Тестовая услуга", price=1000, duration=30, category=self.category
        )

        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.customer = Customer.objects.create(user=self.user, phone="+79123456789")

    def test_valid_booking_form(self):
        """Тест валидной формы бронирования"""
        tomorrow = date.today()

        form_data = {
            "service": self.service.pk,
            "booking_date": tomorrow,
            "booking_time": "10:00",
        }

        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_without_service(self):
        """Тест формы бронирования без услуги"""
        tomorrow = date.today()

        form_data = {"booking_date": tomorrow, "booking_time": "10:00"}

        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("service", form.errors)

    def test_booking_form_widgets(self):
        """Тест виджетов формы бронирования"""
        form = BookingForm()

        # Проверяем, что используются правильные типы полей ввода
        self.assertEqual(form.fields["booking_date"].widget.input_type, "date")
        self.assertEqual(form.fields["booking_time"].widget.input_type, "time")


class CustomerUpdateFormTest(TestCase):
    """Тесты для формы обновления профиля клиента"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.customer = Customer.objects.create(
            user=self.user, phone="+79123456789", discount=10
        )

    def test_valid_customer_update_form(self):
        """Тест валидной формы обновления клиента"""
        form_data = {
            "phone": "+79998887766",
            "car_model": "BMW X5",
            "car_number": "В777ВВ777",
            "discount": 15,
            "notes": "Новые заметки",
        }

        form = CustomerUpdateForm(data=form_data, instance=self.customer)
        self.assertTrue(form.is_valid())

    def test_customer_update_form_save(self):
        """Тест сохранения формы обновления клиента"""
        form_data = {
            "phone": "+79998887766",
            "car_model": "BMW X5",
            "car_number": "В777ВВ777",
            "discount": 15,
            "notes": "Обновленные заметки",
        }

        form = CustomerUpdateForm(data=form_data, instance=self.customer)
        self.assertTrue(form.is_valid())

        updated_customer = form.save()

        self.assertEqual(updated_customer.phone, "+79998887766")
        self.assertEqual(updated_customer.car_model, "BMW X5")
        self.assertEqual(updated_customer.discount, 15)
        self.assertEqual(updated_customer.notes, "Обновленные заметки")

    def test_customer_update_form_invalid_discount(self):
        """Тест формы с недопустимой скидкой"""
        form_data = {
            "phone": "+79998887766",
            "discount": 25,  # Недопустимое значение (не из choices)
        }

        form = CustomerUpdateForm(data=form_data, instance=self.customer)
        self.assertFalse(form.is_valid())
        self.assertIn("discount", form.errors)
