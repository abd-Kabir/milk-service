from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models

from apps.tools.models import Region, District, CompanyType
from config.models import BaseDatesModel


class VerifyCode(BaseDatesModel):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'VerifyToken'


class User(AbstractUser):
    email = models.EmailField(unique=True, default=None, null=True, blank=True, validators=[validate_email, ])
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    middle_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'User'


class UserIndividual(BaseDatesModel):  # физ. лицо
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_individual')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserIndividual'


class UserLegalEntity(BaseDatesModel):  # юр. лицо
    stir = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)

    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_entity')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserLegalEntity'
