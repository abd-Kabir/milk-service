from rest_framework import serializers

from apps.administration.models import Service, SubService


# Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class ServiceNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name_uz',
                  'name_en',
                  'name_ru', ]


# SubService
class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'service', ]


class SubServiceGetSerializer(serializers.ModelSerializer):
    service_display = ServiceNamesSerializer(source='service')

    class Meta:
        model = SubService
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'service',
                  'service_display', ]


# Together
class SubServiceOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class ServiceSubServiceSerializer(serializers.ModelSerializer):
    subservice = SubServiceOnlySerializer(many=True, allow_null=True)

    class Meta:
        model = Service
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'subservice', ]
