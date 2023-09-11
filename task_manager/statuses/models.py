from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Status(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=40, unique=True, blank=False)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')
    