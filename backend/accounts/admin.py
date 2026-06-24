from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "username", "role", "is_verified", "is_active", "created_at"]
    list_filter = ["role", "is_verified", "is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-created_at"]
    fieldsets = UserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role", "phone_number", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Info", {"fields": ("email", "role", "phone_number")}),
    )
