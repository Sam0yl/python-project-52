from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

# Create your models here.


class Task(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),max_length=40, unique=True, blank=False
    )
    description = models.TextField(
        verbose_name=_('Description'), max_length=1000, blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name=_('Author'),
        related_name='author', blank=False
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status'),
        related_name='status', blank=False
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name=_('Executor'),
        related_name='executor', null=True, blank=True
    )
    labels = models.ManyToManyField(
        Label, through='LabelProtection', verbose_name=_('Labels'),
        related_name='labels', blank=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'), auto_now_add=True
    )

    def __str__(self):
        return self.name


class LabelProtection(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
