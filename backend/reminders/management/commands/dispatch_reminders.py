from django.core.management.base import BaseCommand
from reminders.services import send_due_reminders


class Command(BaseCommand):
    help = "Sends all due appointment reminders. Intended to be run via cron every few minutes."

    def handle(self, *args, **options):
        count = send_due_reminders()
        self.stdout.write(self.style.SUCCESS(f"Dispatched {count} reminder(s)."))
