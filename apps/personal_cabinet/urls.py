from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.personal_cabinet.views import PersonalDataRetrieveAPIView, PersonalDataUpdateAPIView, GetInterestsAPIView, \
    PostCategoryModelViewSet

router = DefaultRouter()
router.register(r'post-category', PostCategoryModelViewSet, basename='post_category')

app_name = 'personal_cabinet'
urlpatterns = [
    path('personal/<str:username>/', PersonalDataRetrieveAPIView.as_view(), name='personal'),
    path('update/<str:username>/', PersonalDataUpdateAPIView.as_view(), name='update'),
    path('interests/', GetInterestsAPIView.as_view(), name='interests'),
]
