from django.contrib import admin

from apps.administration.models import UserAdministration, Category, Catalog, SubCatalog, SubCategory, Service, News, \
    SubService, AboutUs, Science, VetCategory, VetSubCategory, FAQ, Banner

admin.site.register(UserAdministration)
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(SubCatalog)
admin.site.register(SubCategory)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(News)
admin.site.register(AboutUs)
admin.site.register(Science)
admin.site.register(VetCategory)
admin.site.register(VetSubCategory)
admin.site.register(FAQ)
admin.site.register(Banner)
