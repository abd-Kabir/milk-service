from rest_framework import serializers

from apps.tools.models import Region, District, CompanyType


class RegionListSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name_uz')

    class Meta:
        model = Region
        fields = ['value',
                  'label', ]


class DistrictListSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name_uz')

    class Meta:
        model = District
        fields = ['value',
                  'label', ]


class CompanyTypeListSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')

    class Meta:
        model = CompanyType
        fields = ['value',
                  'label', ]
