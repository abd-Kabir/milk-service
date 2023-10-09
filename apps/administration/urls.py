from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.administration.views import UserAdminModelViewSet, UserAdminRolesListAPIView

router = DefaultRouter()
router.register(r'admin-user', UserAdminModelViewSet, basename='admin_user')

urlpatterns = [
    path('administration-roles/', UserAdminRolesListAPIView.as_view(), name='admin_roles'),
]

urlpatterns += router.urls
