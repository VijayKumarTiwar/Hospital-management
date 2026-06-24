from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ["appointment", "remind_at", "status", "sent_at"]
    list_filter = ["status"]
