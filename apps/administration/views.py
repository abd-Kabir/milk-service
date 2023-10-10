from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.administration.models import Category, SubCategory, Catalog, SubCatalog, Service, News
from apps.administration.serializer import UserAdminSerializer, UserAdminGetSerializer, UserAdminRolesSerializer, \
    CategorySerializer, CatalogSerializer, SubCatalogSerializer, SubCategorySerializer, SubCategoryGetSerializer, \
    SubCatalogGetSerializer, ServiceSerializer, NewsSerializer
from apps.authentication.models import User


# User-Admin
class UserAdminModelViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__role='ADMIN').exclude(groups__name="SUPERADMIN")
    serializer_class = UserAdminSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return UserAdminGetSerializer(args[0])
        elif self.action == 'list':
            return UserAdminGetSerializer(args[0], many=True)
        return super().get_serializer(*args, **kwargs)


class UserAdminRolesListAPIView(ListAPIView):
    queryset = Group.objects.filter(role='ADMIN')
    serializer_class = UserAdminRolesSerializer


# Category
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# SubCategory
class SubCategoryModelViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return SubCategoryGetSerializer(args[0], many=True)
        elif self.action == 'retrieve':
            return SubCategoryGetSerializer(args[0])
        return super().get_serializer(*args, **kwargs)


# Catalog
class CatalogModelViewSet(ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


# SubCatalog
class SubCatalogModelViewSet(ModelViewSet):
    queryset = SubCatalog.objects.all()
    serializer_class = SubCatalogSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return SubCatalogGetSerializer(args[0], many=True)
        elif self.action == 'retrieve':
            return SubCatalogGetSerializer(args[0])
        return super().get_serializer(*args, **kwargs)


# Service
class ServiceModelViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# News
class NewsModelViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    parser_classes = (MultiPartParser,)
