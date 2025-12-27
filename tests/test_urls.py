from django.test import TestCase
from django.urls import reverse, resolve
from bookings import views as booking_views
from services import views as service_views
from customers import views as customer_views
from pages import views as page_views


class UrlTest(TestCase):
    """Тесты URL маршрутов"""

    def test_index_url(self):
        """Тест URL главной страницы"""
        url = reverse("bookings:index")
        self.assertEqual(url, "/")

        resolver = resolve("/")
        self.assertEqual(resolver.func, booking_views.index)

    def test_service_list_url(self):
        """Тест URL списка услуг"""
        url = reverse("services:service_list")
        self.assertEqual(url, "/services/")

        resolver = resolve("/services/")
        self.assertEqual(resolver.func.__name__, service_views.ServiceListView.__name__)

    def test_create_booking_url(self):
        """Тест URL создания бронирования"""
        url = reverse("bookings:create_booking")
        self.assertEqual(url, "/bookings/")

        resolver = resolve("/bookings/")
        self.assertEqual(
            resolver.func.__name__, booking_views.BookingCreateView.__name__
        )

    def test_my_bookings_url(self):
        """Тест URL моих бронирований"""
        url = reverse("bookings:my_bookings")
        self.assertEqual(url, "/bookings/my/")

        resolver = resolve("/bookings/my/")
        self.assertEqual(resolver.func.__name__, booking_views.MyBookingsView.__name__)

    def test_customer_profile_url(self):
        """Тест URL профиля клиента"""
        url = reverse("customers:profile")
        self.assertEqual(url, "/customers/profile/")

        resolver = resolve("/customers/profile/")
        self.assertEqual(
            resolver.func.__name__, customer_views.CustomerProfileView.__name__
        )

    def test_edit_profile_url(self):
        """Тест URL редактирования профиля"""
        url = reverse("customers:edit_profile")
        self.assertEqual(url, "/customers/profile/edit/")

        resolver = resolve("/customers/profile/edit/")
        self.assertEqual(
            resolver.func.__name__, customer_views.CustomerUpdateView.__name__
        )

    def test_about_url(self):
        """Тест URL страницы 'О нас'"""
        url = reverse("pages:about")
        self.assertEqual(url, "/pages/about/")

        resolver = resolve("/pages/about/")
        self.assertEqual(resolver.func.__name__, page_views.AboutView.__name__)

    def test_contact_url(self):
        """Тест URL страницы 'Контакты'"""
        url = reverse("pages:contact")
        self.assertEqual(url, "/pages/contact/")

        resolver = resolve("/pages/contact/")
        self.assertEqual(resolver.func.__name__, page_views.ContactView.__name__)

    def test_price_list_url(self):
        """Тест URL прайс-листа"""
        url = reverse("pages:price_list")
        self.assertEqual(url, "/pages/price-list/")

        resolver = resolve("/pages/price-list/")
        self.assertEqual(resolver.func.__name__, page_views.PriceListView.__name__)

    def test_login_url(self):
        """Тест URL входа"""
        url = reverse("login")
        self.assertEqual(url, "/auth/login/")

    def test_logout_url(self):
        """Тест URL выхода"""
        url = reverse("logout")
        self.assertEqual(url, "/auth/logout/")

    def test_registration_url(self):
        """Тест URL регистрации"""
        url = reverse("registration")
        self.assertEqual(url, "/auth/registration/")

        resolver = resolve("/auth/registration/")
        self.assertEqual(
            resolver.func.__name__, booking_views.UserRegistrationView.__name__
        )
