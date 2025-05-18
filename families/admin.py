from django.contrib import admin
from .models import FamilyGroup, FamilyMembership, Question, Answer, LogEntry, AIKnowledgeBase


# Register your models here.
admin.site.register(FamilyGroup)
admin.site.register(FamilyMembership)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LogEntry)
admin.site.register(AIKnowledgeBase)