from django.contrib import admin

from apps.authentication.models import UserIndividual, UserLegalEntity, User, UserAdmin

# admin.site.register(User)
admin.site.register(UserIndividual)
admin.site.register(UserLegalEntity)
admin.site.register(UserAdmin)


class UserAdmin(admin.ModelAdmin):
    list_filter = ["first_name"]


admin.site.register(User, UserAdmin)
