from django.contrib import admin

from apps.tools.models import CompanyType, Region, District

admin.site.register(CompanyType)
admin.site.register(Region)
admin.site.register(District)
