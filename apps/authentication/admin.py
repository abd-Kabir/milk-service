from django.contrib import admin

from apps.authentication.models import UserIndividual, UserLegalEntity, User

admin.site.register(User)
admin.site.register(UserIndividual)
admin.site.register(UserLegalEntity)
