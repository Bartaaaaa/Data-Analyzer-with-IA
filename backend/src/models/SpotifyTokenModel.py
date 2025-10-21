from django.db import models

from django.conf import settings

class SpotifyToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"SpotifyToken({self.user.username})"