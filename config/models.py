from django.db import models


class BaseDatesModel(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True)  # дата создания
    updated_at = models.DateTimeField(null=True, auto_now_add=True)  # дата обновления

    class Meta:
        abstract = True
