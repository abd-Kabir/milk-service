from django.db import models

from apps.administration.models import SubCategory, SubCatalog, SubService, Category, Catalog, Service
from apps.authentication.models import User
from apps.tools.utils.hash import hash_filename
from config.models import BaseDatesModel


class PostCategory(BaseDatesModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_category')

    class Meta:
        db_table = 'PostCategory'


class PostCatalog(BaseDatesModel):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_catalog')

    class Meta:
        db_table = 'PostCatalog'


class PostService(BaseDatesModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_service')

    class Meta:
        db_table = 'PostService'


class Application(BaseDatesModel):
    ACCEPTED = "ACCEPTED"
    WAITING = "WAITING"
    APPLICATION_STATUS = [
        (ACCEPTED, ACCEPTED),
        (WAITING, WAITING),
    ]
    status = models.CharField(max_length=255, choices=APPLICATION_STATUS, default=WAITING)

    ZOOM = "ZOOM"
    PHONE = "PHONE"
    OFFLINE = "OFFLINE"
    APPLICATION_TYPE = [
        (ZOOM, ZOOM),
        (PHONE, PHONE),
        (OFFLINE, OFFLINE),
    ]
    app_type = models.CharField(max_length=10, choices=APPLICATION_TYPE, default=PHONE)

    zoom_link = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    post_category = models.ForeignKey(PostCategory,
                                      on_delete=models.SET_NULL,
                                      related_name='applications',
                                      null=True, blank=True)
    post_catalog = models.ForeignKey(PostCatalog,
                                     on_delete=models.SET_NULL,
                                     related_name='applications',
                                     null=True, blank=True)
    post_service = models.ForeignKey(PostService,
                                     on_delete=models.SET_NULL,
                                     related_name='applications',
                                     null=True, blank=True)
    buyer = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='applications')

    class Meta:
        db_table = 'Application'
