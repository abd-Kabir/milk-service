from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.administration.views import UserAdminModelViewSet, UserAdminRolesListAPIView, CategoryModelViewSet, \
    SubCategoryModelViewSet, CatalogModelViewSet, SubCatalogModelViewSet, ServiceModelViewSet, NewsModelViewSet, \
    BannerModelViewSet, GetTypesAPIView, SubServiceModelViewSet

router = DefaultRouter()
router.register(r'admin-user', UserAdminModelViewSet, basename='admin_user')
router.register(r'category', CategoryModelViewSet, basename='category')
router.register(r'subcategory', SubCategoryModelViewSet, basename='subcategory')
router.register(r'catalog', CatalogModelViewSet, basename='catalog')
router.register(r'subcatalog', SubCatalogModelViewSet, basename='subcatalog')
router.register(r'service', ServiceModelViewSet, basename='service')
router.register(r'subservice', SubServiceModelViewSet, basename='subservice')
router.register(r'news', NewsModelViewSet, basename='news')
router.register(r'banner', BannerModelViewSet, basename='banner')

app_name = 'administration'
urlpatterns = [
    path('administration-roles/', UserAdminRolesListAPIView.as_view(), name='admin_roles'),
    path('types/', GetTypesAPIView.as_view(), name='types'),
]

urlpatterns += router.urls
