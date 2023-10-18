from django.contrib.auth.models import Group
from django.db import models

from apps.authentication.models import User
from apps.tools.utils.hash import hash_filename
from config.models import BaseDatesModel

USER = 'USER'
ADMIN = 'ADMIN'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN)
]
Group.add_to_class('role', models.CharField(choices=ROLE_CHOICES, max_length=10, null=True, blank=True))


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


class SubService(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='subservice')

    class Meta:
        db_table = 'SubService'


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


class Banner(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    photo = models.FileField(upload_to=hash_filename)

    class Meta:
        db_table = 'Banner'


class AboutUs(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    photo = models.FileField(upload_to=hash_filename)

    class Meta:
        db_table = 'AboutUs'


class Science(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    video = models.TextField()
    photo = models.FileField(upload_to=hash_filename)
    file = models.FileField(upload_to=hash_filename)

    class Meta:
        db_table = 'Science'


class VetCategory(BaseDatesModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    class Meta:
        db_table = 'VetCategory'


class VetSubCategory(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=hash_filename, null=True, blank=True)
    photo = models.FileField(upload_to=hash_filename, null=True, blank=True)

    vet_category = models.ForeignKey(VetCategory, on_delete=models.CASCADE, related_name='vet_subcategory')

    class Meta:
        db_table = 'VetSubCategory'


class FAQ(BaseDatesModel):
    question_uz = models.CharField(max_length=255)
    question_ru = models.CharField(max_length=255)
    question_en = models.CharField(max_length=255)
    answer_uz = models.TextField()
    answer_ru = models.TextField()
    answer_en = models.TextField()

    class Meta:
        db_table = 'FAQ'


class HintCategory(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    class Meta:
        db_table = 'HintCategory'


class HintSubCategory(BaseDatesModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    photo = models.FileField(upload_to=hash_filename, null=True, blank=True)
    video = models.URLField(max_length=255, null=True, blank=True)

    hint_category = models.ForeignKey(HintCategory, on_delete=models.CASCADE, related_name='vet_subcategory')

    class Meta:
        db_table = 'HintSubCategory'
