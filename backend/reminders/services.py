from django.utils import timezone
from .models import Reminder
from notifications.services import create_notification
from notifications.models import Notification


def send_due_reminders():
    """
    Finds all SCHEDULED reminders whose remind_at has passed and dispatches
    a notification to the patient. Intended to be run periodically
    (e.g. via a cron job, Celery beat task, or management command).
    """
    due = Reminder.objects.filter(status=Reminder.Status.SCHEDULED, remind_at__lte=timezone.now())
    sent_count = 0
    for reminder in due.select_related("appointment__patient__user", "appointment__doctor__user"):
        appointment = reminder.appointment
        create_notification(
            recipient=appointment.patient.user,
            title="Upcoming Appointment Reminder",
            message=reminder.message or (
                f"You have an appointment with Dr. {appointment.doctor.user.get_full_name()} "
                f"on {appointment.scheduled_at.strftime('%Y-%m-%d %H:%M')}."
            ),
            notification_type=Notification.NotificationType.REMINDER,
            related_object_id=appointment.id,
        )
        reminder.status = Reminder.Status.SENT
        reminder.sent_at = timezone.now()
        reminder.save(update_fields=["status", "sent_at"])
        sent_count += 1
    return sent_count
