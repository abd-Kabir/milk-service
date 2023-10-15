from django.contrib import admin

from apps.personal_cabinet.models import Application, PostService, PostCatalog, PostCategory

admin.site.register(PostCategory)
admin.site.register(PostCatalog)
admin.site.register(PostService)
admin.site.register(Application)
