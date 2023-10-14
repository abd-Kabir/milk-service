from django.contrib import admin

from apps.authentication.models import UserIndividual, UserLegalEntity, User, UserBuyer

admin.site.register(UserIndividual)
admin.site.register(UserLegalEntity)
admin.site.register(User)
admin.site.register(UserBuyer)
