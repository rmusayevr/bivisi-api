from django.db import models
from account.models import User


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.recipient}'s notification"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
