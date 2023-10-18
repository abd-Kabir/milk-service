from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.administration.views import UserAdminModelViewSet, UserAdminRolesListAPIView, CategoryModelViewSet, \
    SubCategoryModelViewSet, CatalogModelViewSet, SubCatalogModelViewSet, ServiceModelViewSet, NewsModelViewSet, \
    BannerModelViewSet, GetCatTypesAPIView, SubServiceModelViewSet, GetServiceTypesAPIView, AboutUsModelViewSet, \
    ScienceModelViewSet, VetSubCategoryModelViewSet, VetCategoryModelViewSet, VetCategorySubListAPIView, \
    FAQModelViewSet, HintSubCategoryModelViewSet, HintCategoryModelViewSet, HintCategorySubListAPIView

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
router.register(r'about-us', AboutUsModelViewSet, basename='about_us')
router.register(r'science', ScienceModelViewSet, basename='science')
router.register(r'faq', FAQModelViewSet, basename='faq')
router.register(r'vet-category', VetCategoryModelViewSet, basename='vet_category')
router.register(r'vet-subcategory', VetSubCategoryModelViewSet, basename='vet_subcategory')
router.register(r'hint-category', HintCategoryModelViewSet, basename='hint_category')
router.register(r'hint-subcategory', HintSubCategoryModelViewSet, basename='hint_subcategory')

app_name = 'administration'
urlpatterns = [
    path('administration-roles/', UserAdminRolesListAPIView.as_view(), name='admin_roles'),
    path('cat-types/', GetCatTypesAPIView.as_view(), name='cat_types'),
    path('service-types/', GetServiceTypesAPIView.as_view(), name='service_types'),
    path('vet-child/<int:category_id>/', VetCategorySubListAPIView.as_view(), name='vet_child'),
    path('hint-child/<int:category_id>/', HintCategorySubListAPIView.as_view(), name='hint_child'),
]

urlpatterns += router.urls
