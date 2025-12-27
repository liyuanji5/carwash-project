from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bookings.views import UserRegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookings.urls")),
    path("services/", include("services.urls")),
    path("customers/", include("customers.urls")),
    path("employees/", include("employees.urls")),
    path("pages/", include("pages.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/registration/", UserRegistrationView.as_view(), name="registration"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "pages.views.permission_denied"
handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
