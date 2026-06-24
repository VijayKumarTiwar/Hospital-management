from django.contrib import admin
from .models import SymptomEntry, ChatSession, ChatMessage

admin.site.register(SymptomEntry)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
