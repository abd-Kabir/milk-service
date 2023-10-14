from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.personal_cabinet.views import PersonalDataRetrieveAPIView, PersonalDataUpdateAPIView, GetInterestsAPIView, \
    PostCategoryModelViewSet, PostServiceModelViewSet, PostCatalogModelViewSet

router = DefaultRouter()
router.register(r'post-category', PostCategoryModelViewSet, basename='post_category')
router.register(r'post-catalog', PostCatalogModelViewSet, basename='post_catalog')
router.register(r'post-service', PostServiceModelViewSet, basename='post_service')

app_name = 'personal_cabinet'
urlpatterns = [
    path('personal/', PersonalDataRetrieveAPIView.as_view(), name='personal'),
    path('update/', PersonalDataUpdateAPIView.as_view(), name='update'),
    path('interests/', GetInterestsAPIView.as_view(), name='interests'),
]

urlpatterns += router.urls
