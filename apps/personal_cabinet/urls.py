from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.personal_cabinet.views import PersonalDataRetrieveAPIView, PersonalDataUpdateAPIView, GetAllInterestsAPIView, \
    PostCategoryModelViewSet, PostServiceModelViewSet, PostCatalogModelViewSet

router = DefaultRouter()
router.register(r'post-category', PostCategoryModelViewSet, basename='post_category')
router.register(r'post-catalog', PostCatalogModelViewSet, basename='post_catalog')
router.register(r'post-service', PostServiceModelViewSet, basename='post_service')

app_name = 'personal_cabinet'
urlpatterns = [
    path('personal/<str:username>/', PersonalDataRetrieveAPIView.as_view(), name='personal'),
    path('update/<str:username>/', PersonalDataUpdateAPIView.as_view(), name='update'),
    path('interests/', GetAllInterestsAPIView.as_view(), name='interests'),
]

urlpatterns += router.urls
