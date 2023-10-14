from django.contrib import admin

from apps.administration.models import UserAdministration, Category, Catalog, SubCatalog, SubCategory, Service, News, \
    SubService

admin.site.register(UserAdministration)
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(SubCatalog)
admin.site.register(SubCategory)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(News)
