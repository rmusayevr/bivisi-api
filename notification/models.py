from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product, ProductComment
from user.models import User
from services.mixins import DateMixin


class Notification(DateMixin):
    class NotificationTypeChoices(models.TextChoices):
        LIKE = "Like", _("Like")
        COMMENT = "Comment", _("Comment")
        SUBSCRIBE = "Subscribe", _("Subscribe")

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
        related_name="recipient_notifications",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Sender"),
        related_name="sender_notifications",
    )
    message = models.TextField(verbose_name=_("Message"))
    notification_type = models.CharField(
        verbose_name=_("Notification Type"),
        max_length=20,
        choices=NotificationTypeChoices.choices,
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    comment_id = models.ForeignKey(
        ProductComment, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Notification for {self.recipient.username} from {self.sender.username} - {self.notification_type}"

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]
