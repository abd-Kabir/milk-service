from django.db import models

from apps.administration.models import SubCategory, SubCatalog, SubService
from apps.authentication.models import User
from apps.tools.utils.hash import hash_filename
from config.models import BaseDatesModel


class PostCategory(BaseDatesModel):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    age = models.SmallIntegerField()
    weight = models.FloatField()
    amount = models.SmallIntegerField()
    price = models.CharField(max_length=20)
    address = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    photo = models.FileField(upload_to=hash_filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PostCategory'


class PostCatalog(BaseDatesModel):
    subcatalog = models.ForeignKey(SubCatalog, on_delete=models.CASCADE)
    volume = models.IntegerField()
    amount = models.SmallIntegerField()
    price = models.CharField(max_length=20)
    address = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    photo = models.FileField(upload_to=hash_filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PostCatalog'


class PostService(BaseDatesModel):
    subservice = models.ForeignKey(SubService, on_delete=models.CASCADE)
    price = models.CharField(max_length=20)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    photo = models.FileField(upload_to=hash_filename)

    OFFLINE = 'OFFLINE'
    PHONE = 'PHONE'
    ZOOM = 'ZOOM'
    SERVICE_TYPE_CHOICE = [
        (OFFLINE, OFFLINE),
        (PHONE, PHONE),
        (ZOOM, ZOOM),
    ]
    service_type = models.CharField(max_length=7, choices=SERVICE_TYPE_CHOICE, default=OFFLINE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PostService'
