from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.personal_cabinet.views import PersonalDataRetrieveAPIView, PersonalDataUpdateAPIView, \
    PostCategoryModelViewSet, PostServiceModelViewSet, PostCatalogModelViewSet, CombinedPostAPIView, \
    ApplicationCreateAPIView

router = DefaultRouter()
router.register(r'post-category', PostCategoryModelViewSet, basename='post_category')
router.register(r'post-catalog', PostCatalogModelViewSet, basename='post_catalog')
router.register(r'post-service', PostServiceModelViewSet, basename='post_service')

app_name = 'personal_cabinet'
urlpatterns = [
    path('personal/', PersonalDataRetrieveAPIView.as_view(), name='personal'),
    path('update/', PersonalDataUpdateAPIView.as_view(), name='update'),
    # path('interests/', GetInterestsAPIView.as_view(), name='interests'),
    path('combined-posts/', CombinedPostAPIView.as_view(), name='combined_posts'),
    path('apply/', ApplicationCreateAPIView.as_view(), name='apply'),
]

urlpatterns += router.urls
