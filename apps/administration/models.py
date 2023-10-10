from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models

from apps.authentication.models import User
from config.models import BaseDatesModel

USER = 'USER'
ADMIN = 'ADMIN'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN)
]
Group.add_to_class('role', models.CharField(choices=ROLE_CHOICES, max_length=10, null=True, blank=True))


def hash_filename(instance, filename):
    now = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    return f"uploads/{now}_{filename}"


class UserAdministration(BaseDatesModel):  # administration
    position = models.CharField(max_length=100, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_admin')

    class Meta:
        db_table = 'UserAdministration'


class Category(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    class Meta:
        db_table = 'Category'


class SubCategory(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    class Meta:
        db_table = 'SubCategory'


class Catalog(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    class Meta:
        db_table = 'Catalog'


class SubCatalog(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='subcatalog')

    class Meta:
        db_table = 'SubCatalog'


class Service(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    class Meta:
        db_table = 'Service'


class News(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    photo = models.FileField(upload_to=hash_filename)

    class Meta:
        db_table = 'News'
