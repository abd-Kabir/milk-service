from django.contrib import admin

from apps.tools.models import CompanyType, Region, District

admin.site.register(CompanyType)
admin.site.register(Region)


class DistrictAdmin(admin.ModelAdmin):
    list_filter = ["region_id"]


admin.site.register(District, DistrictAdmin)
