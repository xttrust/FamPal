from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.jpg')  # You need MEDIA settings

    def __str__(self):
        return self.user.username
