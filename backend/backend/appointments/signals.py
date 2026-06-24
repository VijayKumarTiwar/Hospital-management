from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment


@receiver(post_save, sender=Appointment)
def on_appointment_created(sender, instance, created, **kwargs):
    from notifications.services import create_notification
    from notifications.models import Notification
    from reminders.models import Reminder

    if created:
        # Notify both parties.
        create_notification(
            recipient=instance.patient.user,
            title="Appointment Booked",
            message=f"Your appointment with Dr. {instance.doctor.user.get_full_name()} is scheduled for {instance.scheduled_at.strftime('%Y-%m-%d %H:%M')}.",
            notification_type=Notification.NotificationType.APPOINTMENT,
            related_object_id=instance.id,
        )
        create_notification(
            recipient=instance.doctor.user,
            title="New Appointment",
            message=f"New appointment booked by {instance.patient.user.get_full_name()} for {instance.scheduled_at.strftime('%Y-%m-%d %H:%M')}.",
            notification_type=Notification.NotificationType.APPOINTMENT,
            related_object_id=instance.id,
        )
        # Auto-schedule a reminder 1 hour before the appointment, if that's in the future.
        remind_at = instance.scheduled_at - timedelta(hours=1)
        Reminder.objects.create(appointment=instance, remind_at=remind_at)
