from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import validate_email
from django.db import models

from apps.tools.models import Region, District, CompanyType
from apps.tools.utils.hash import hash_filename
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

    NONE = None
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = [
        (NONE, NONE),
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=NONE, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    avatar = models.FileField(upload_to=hash_filename, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'


class UserBuyer(BaseDatesModel):  # покупщик
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_buyer')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserBuyer'


class UserIndividual(BaseDatesModel):  # физ. лицо
    service_certificate = models.FileField(upload_to=hash_filename, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_individual')
    subcatalog = models.ManyToManyField('administration.SubCatalog', related_name='user_individual')
    subcategory = models.ManyToManyField('administration.SubCategory', related_name='user_individual')
    subservice = models.ManyToManyField('administration.SubService', related_name='user_individual')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserIndividual'


class UserLegalEntity(BaseDatesModel):  # юр. лицо
    stir = models.CharField(max_length=9, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True, blank=True)

    service_certificate = models.FileField(upload_to=hash_filename, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_entity')
    subcatalog = models.ManyToManyField('administration.SubCatalog', related_name='user_entity')
    subcategory = models.ManyToManyField('administration.SubCategory', related_name='user_entity')
    subservice = models.ManyToManyField('administration.SubService', related_name='user_entity')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserLegalEntity'
