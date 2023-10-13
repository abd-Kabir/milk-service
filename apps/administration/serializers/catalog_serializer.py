from rest_framework import serializers

from apps.administration.models import Catalog, SubCatalog


# Catalog
class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class CatalogNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['name_uz',
                  'name_en',
                  'name_ru', ]


# SubCatalog
class SubCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCatalog
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'catalog', ]


class SubCatalogGetSerializer(serializers.ModelSerializer):
    catalog_display = CatalogNamesSerializer(source='catalog')

    class Meta:
        model = SubCatalog
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'catalog',
                  'catalog_display', ]


# Together
class SubCatalogOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCatalog
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class CatalogSubCatalogSerializer(serializers.ModelSerializer):
    subcatalog = SubCatalogOnlySerializer(many=True, allow_null=True)

    class Meta:
        model = Catalog
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'subcatalog', ]
