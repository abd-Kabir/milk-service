from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.administration.views import UserAdminModelViewSet, UserAdminRolesListAPIView, CategoryModelViewSet, \
    SubCategoryModelViewSet

router = DefaultRouter()
router.register(r'admin-user', UserAdminModelViewSet, basename='admin_user')
router.register(r'category', CategoryModelViewSet, basename='category')
router.register(r'subcategory', SubCategoryModelViewSet, basename='subcategory')

app_name = 'administration'
urlpatterns = [
    path('administration-roles/', UserAdminRolesListAPIView.as_view(), name='admin_roles'),
]

urlpatterns += router.urls
