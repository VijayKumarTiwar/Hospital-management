from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hospital Management System API is Running Successfully!")

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Hospital Management API",
      default_version='v1',
      description="API documentation for Ai-healthcare",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    path("api/accounts/", include("accounts.urls")),
    path("api/", include("doctors.urls")),
    path("api/", include("patients.urls")),
    path("api/", include("appointments.urls")),
    path("api/chatbot/", include("chatbot.urls")),
    path("api/prediction/", include("prediction.urls")),
    path("api/", include("notifications.urls")),
    path("api/", include("reminders.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/dashboard/", include("dashboard.urls")),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]