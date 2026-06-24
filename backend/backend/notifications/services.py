from .models import Notification


def create_notification(recipient, title, message, notification_type=Notification.NotificationType.SYSTEM, related_object_id=None):
    """Helper used by other apps (appointments, reminders, reports) to push a notification."""
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_id=related_object_id,
    )
