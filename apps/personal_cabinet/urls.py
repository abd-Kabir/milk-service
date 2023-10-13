from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.personal_cabinet.views import PersonalDataModelViewSet

router = DefaultRouter()

router.register(r'personal', PersonalDataModelViewSet, basename='personal')

app_name = 'personal_cabinet'
urlpatterns = [
    # path()
]

urlpatterns += router.urls
