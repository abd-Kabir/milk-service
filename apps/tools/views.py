from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

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
