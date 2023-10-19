from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCatalog, PostCategory, PostService, Application
from apps.tools.models import Region, District, CompanyType
from apps.tools.serializer import RegionListSerializer, DistrictListSerializer, CompanyTypeListSerializer


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    permission_classes = [AllowAny, ]


class DistrictListAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictListSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return super().get_queryset().filter(region_id_id=self.kwargs['pk'])


class CompanyTypeListAPIView(ListAPIView):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeListSerializer
    permission_classes = [AllowAny, ]


class DashboardAPIView(APIView):
    def get(self, request):
        seller_count = User.objects.filter(groups__name='SELLER').count()
        service_count = User.objects.filter(groups__name='SERVICE').count()
        buyer_count = User.objects.filter(groups__name='BUYER').count()

        post_category_count = PostCategory.objects.count()
        post_catalog_count = PostCatalog.objects.count()
        post_service_count = PostService.objects.count()

        application_category = Application.objects.filter(post_category__isnull=False).count()
        application_catalog = Application.objects.filter(post_catalog__isnull=False).count()
        application_service = Application.objects.filter(post_service__isnull=False).count()
        return Response({
            "users": {
                "total": seller_count + service_count + buyer_count,
                "seller": seller_count,
                "service": service_count,
                "buyer": buyer_count
            },
            "posts": {
                "total": post_category_count + post_catalog_count + post_service_count,
                "category": post_category_count,
                "catalog": post_catalog_count,
                "service": post_service_count
            },
            "applications": {
                "total": application_category + application_catalog + application_service,
                "category": application_category,
                "catalog": application_catalog,
                "service": application_service
            }
        })
