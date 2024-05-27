from django.db import models
from account.models import User
from product.models import ProductVideoType
from services.mixins import DateMixin
from django.utils.translation import gettext_lazy as _



class UserHistory(DateMixin):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_history')
    product_video_type = models.ForeignKey(ProductVideoType, verbose_name=_("Product Video Type"), on_delete=models.CASCADE, related_name='history_video_type')
    watch_date = models.DateTimeField(_("Watch date"))

    def __str__(self):
        return f"{self.user.username} - {self.product_video_type.pk}"

    class Meta:
        verbose_name = 'User History'
        verbose_name_plural = 'User History'
        unique_together = ('user', 'product_video_type')
        indexes = [
            models.Index(fields=['user', 'product_video_type']),
        ]
