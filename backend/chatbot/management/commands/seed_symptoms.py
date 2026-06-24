from django.core.management.base import BaseCommand
from chatbot.engine import seed_symptoms


class Command(BaseCommand):
    help = "Seeds the chatbot's symptom knowledge base with default entries."

    def handle(self, *args, **options):
        count = seed_symptoms()
        self.stdout.write(self.style.SUCCESS(f"Seeded {count} new symptom entries."))
