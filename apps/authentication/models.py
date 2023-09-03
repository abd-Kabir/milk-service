from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseDatesModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'User'


class UserIndividual(BaseDatesModel):  # физ. лицо
    class Meta:
        db_table = 'UserIndividual'


class UserLegalEntity(BaseDatesModel):  # юр. лицо
    class Meta:
        db_table = 'UserLegalEntity'
