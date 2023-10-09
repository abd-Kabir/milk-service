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


class UserAdministration(BaseDatesModel):  # administration
    position = models.CharField(max_length=100, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_admin')

    class Meta:
        db_table = 'UserAdministration'


# class Category(BaseDatesModel):
#     name
