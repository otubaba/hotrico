from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Home page
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    # Accounts
    path("account/", include("accounts.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Academics
    path("academics/", include("academics.urls")),

    # Communication
    path("communication/", include("communication.urls")),

    # Students
    path("students/", include("students.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Optional: Serve static files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
