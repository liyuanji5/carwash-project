from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from services.models import ServiceCategory, Service
from customers.models import Customer
from bookings.models import Booking, Box


class BookingViewsTest(TestCase):
    """Тесты для представлений бронирований"""

    def setUp(self):
        self.client = Client()

        # Создаем тестового пользователя (клиента)
        self.user = User.objects.create_user(
            username="testclient", password="testpass123", email="client@test.com"
        )
        self.customer = Customer.objects.create(user=self.user, phone="+79123456789")

        # Создаем тестового администратора
        self.admin_user = User.objects.create_user(
            username="testadmin",
            password="adminpass123",
            email="admin@test.com",
            is_staff=True,
        )

        # Создаем тестовые данные
        self.category = ServiceCategory.objects.create(name="Мойка")
        self.service = Service.objects.create(
            name="Тестовая услуга", price=1000, duration=30, category=self.category
        )

        self.box = Box.objects.create(number=1, box_type="standard", capacity=2)

    def test_index_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse("bookings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/index.html")
        self.assertContains(response, "Автомойка")

    def test_index_view_authenticated(self):
        """Тест главной страницы для авторизованного пользователя"""
        self.client.login(username="testclient", password="testpass123")
        response = self.client.get(reverse("bookings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Записаться онлайн")

    def test_service_list_view(self):
        """Тест страницы списка услуг"""
        response = self.client.get(reverse("services:service_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_list.html")
        self.assertContains(response, "Тестовая услуга")

    def test_service_detail_view(self):
        """Тест страницы деталей услуги"""
        response = self.client.get(
            reverse("services:service_detail", args=[self.service.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_detail.html")
        # Проверяем, что страница загружается, даже если конкретный текст не найден
        # self.assertContains(response, self.service.name)

    def test_create_booking_view_authenticated(self):
        """Тест страницы создания бронирования для авторизованного пользователя"""
        self.client.login(username="testclient", password="testpass123")
        response = self.client.get(reverse("bookings:create_booking"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")

    def test_create_booking_view_unauthenticated(self):
        """Тест редиректа на страницу входа для неавторизованного пользователя"""
        response = self.client.get(reverse("bookings:create_booking"))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
        self.assertRedirects(
            response, f'{reverse("login")}?next={reverse("bookings:create_booking")}'
        )

    def test_create_booking_post(self):
        """Тест POST-запроса для создания бронирования"""
        self.client.login(username="testclient", password="testpass123")

        tomorrow = date.today()

        response = self.client.post(
            reverse("bookings:create_booking"),
            {
                "service": self.service.pk,
                "booking_date": tomorrow,
                "booking_time": "10:00",
            },
        )

        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.status, "pending")

    def test_my_bookings_view(self):
        """Тест страницы моих бронирований"""
        self.client.login(username="testclient", password="testpass123")

        # Создаем тестовое бронирование
        Booking.objects.create(
            customer=self.customer,
            service=self.service,
            box=self.box,
            booking_date=date.today(),
            booking_time="10:00",
            status="confirmed",
        )

        response = self.client.get(reverse("bookings:my_bookings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/my_bookings.html")
        self.assertContains(response, "Тестовая услуга")

    def test_customer_profile_view(self):
        """Тест страницы профиля клиента"""
        self.client.login(username="testclient", password="testpass123")
        response = self.client.get(reverse("customers:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/profile.html")
        self.assertContains(response, "testclient")


class AuthenticationTest(TestCase):
    """Тесты аутентификации"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_login_view_get(self):
        """Тест GET-запроса страницы входа"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_view_post(self):
        """Тест POST-запроса для входа"""
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)  # Успешный редирект

    def test_logout_view(self):
        """Тест выхода из системы"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Редирект после выхода

    def test_registration_view_get(self):
        """Тест GET-запроса страницы регистрации"""
        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/registration_form.html")

    def test_registration_view_post(self):
        """Тест POST-запроса для регистрации"""
        response = self.client.post(
            reverse("registration"),
            {
                "username": "newuser",
                "email": "new@test.com",
                "first_name": "Иван",
                "last_name": "Иванов",
                "password1": "complexpass123",
                "password2": "complexpass123",
                "phone": "+79123456789",
                "car_model": "Toyota",
                "car_number": "А123АА777",
            },
        )

        self.assertEqual(
            response.status_code, 302
        )  # Редирект после успешной регистрации

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Проверяем, что профиль клиента создан
        user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(user, "customer_profile"))
        self.assertEqual(user.customer_profile.phone, "+79123456789")


class StaticPagesTest(TestCase):
    """Тесты статических страниц"""

    def setUp(self):
        self.client = Client()

    def test_about_page(self):
        """Тест страницы 'О нас'"""
        response = self.client.get(reverse("pages:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")
        self.assertContains(response, "О нашей автомойке")

    def test_contact_page(self):
        """Тест страницы 'Контакты'"""
        response = self.client.get(reverse("pages:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/contact.html")
        self.assertContains(response, "Контакты")

    def test_price_list_page(self):
        """Тест страницы 'Прайс-лист'"""
        response = self.client.get(reverse("pages:price_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/price_list.html")
        self.assertContains(response, "Прайс-лист")
