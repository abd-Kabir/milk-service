# Category
from rest_framework import serializers

from apps.administration.models import Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class CategoryNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name_uz',
                  'name_en',
                  'name_ru', ]


# SubCategory
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'category', ]


class SubCategoryGetSerializer(serializers.ModelSerializer):
    category_display = CategoryNamesSerializer(source='category')

    class Meta:
        model = SubCategory
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'category',
                  'category_display', ]


# Together
class SubCategoryOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru', ]


class CategorySubCategorySerializer(serializers.ModelSerializer):
    subcategory = SubCategoryOnlySerializer(many=True, allow_null=True)

    class Meta:
        model = Category
        fields = ['id',
                  'name_uz',
                  'name_en',
                  'name_ru',
                  'subcategory', ]
