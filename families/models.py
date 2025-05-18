from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class FamilyGroup(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_family_groups')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class FamilyMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_memberships')
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'family_group')

    def __str__(self):
        return f"{self.user} in {self.family_group}"

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    family_group = models.ForeignKey(
        FamilyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions'
    )
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Question by {self.user} in {self.family_group}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='answers')  # could be AI or human
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        author = "AI" if self.is_ai_generated else (self.user.username if self.user else "Unknown")
        return f"Answer by {author}"

class LogEntry(models.Model):
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='log_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_log_entries')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} did {self.action} at {self.timestamp}"


class AIKnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    