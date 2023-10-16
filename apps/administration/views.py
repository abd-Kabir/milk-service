from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.administration.models import Category, SubCategory, Catalog, SubCatalog, Service, News, Banner, SubService, \
    AboutUs, Science, VetCategory, VetSubCategory, FAQ
from apps.administration.serializers.another_serializer import UserAdminSerializer, UserAdminGetSerializer, \
    UserAdminRolesSerializer, NewsSerializer, BannerSerializer, AboutUsSerializer, ScienceSerializer, \
    VetCategorySerializer, VetSubCategorySerializer, FAQSerializer
from apps.administration.serializers.catalog_serializer import CatalogSerializer, SubCatalogSerializer, \
    SubCatalogGetSerializer, CatalogSubCatalogSerializer
from apps.administration.serializers.category_serializer import CategorySerializer, SubCategorySerializer, \
    SubCategoryGetSerializer, CategorySubCategorySerializer
from apps.administration.serializers.service_serializer import ServiceSerializer, SubServiceSerializer, \
    SubServiceGetSerializer, ServiceSubServiceSerializer

from apps.authentication.models import User
from config.utils.permissions import LandingPage


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


# SubService
class SubServiceModelViewSet(ModelViewSet):
    queryset = SubService.objects.all()
    serializer_class = SubServiceSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return SubServiceGetSerializer(args[0], many=True)
        elif self.action == 'retrieve':
            return SubServiceGetSerializer(args[0])
        return super().get_serializer(*args, **kwargs)


class GetCatTypesAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        category_queryset = Category.objects.all()
        category_serializer = CategorySubCategorySerializer(category_queryset, many=True)
        catalog_queryset = Catalog.objects.all()
        catalog_serializer = CatalogSubCatalogSerializer(catalog_queryset, many=True)
        return Response({
            "category": category_serializer.data,
            "catalog": catalog_serializer.data
        })


class GetServiceTypesAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        service_queryset = Service.objects.all()
        service_serializer = ServiceSubServiceSerializer(service_queryset, many=True)
        return Response({
            "service": service_serializer.data
        })


# News
class NewsModelViewSet(ModelViewSet):
    queryset = News.objects.order_by('-id')
    serializer_class = NewsSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [LandingPage, ]


# Banner
class BannerModelViewSet(ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [LandingPage, ]


# AboutUs
class AboutUsModelViewSet(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [LandingPage, ]


# Science
class ScienceModelViewSet(ModelViewSet):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [LandingPage, ]


# FAQ
class FAQModelViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [LandingPage, ]


# Vet
class VetCategoryModelViewSet(ModelViewSet):
    queryset = VetCategory.objects.all()
    serializer_class = VetCategorySerializer
    permission_classes = [LandingPage, ]


class VetSubCategoryModelViewSet(ModelViewSet):
    queryset = VetSubCategory.objects.all()
    serializer_class = VetSubCategorySerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [LandingPage, ]


class VetCategorySubListAPIView(ListAPIView):
    serializer_class = VetSubCategorySerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        category_id = self.kwargs['category_id']  # Get the category_id from the URL parameter
        return VetSubCategory.objects.filter(vet_category=category_id)
