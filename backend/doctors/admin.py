from django.contrib import admin
from .models import Doctor, Specialization, DoctorAvailability

admin.site.register(Specialization)
admin.site.register(DoctorAvailability)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["user", "license_number", "years_of_experience", "consultation_fee", "is_available"]
    list_filter = ["is_available", "specializations"]
    search_fields = ["user__first_name", "user__last_name", "license_number"]
