from datetime import datetime

from rest_framework import serializers

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory


class UserEntityPersonalDataSerializer(serializers.ModelSerializer):
    stir = serializers.CharField(source='user_entity.stir')
    company_name = serializers.CharField(source='user_entity.company_name')
    position = serializers.CharField(source='user_entity.position')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    def update(self, instance, validated_data):
        instance.user_entity.position = validated_data['user_entity']['position']
        instance.user_entity.updated_at = datetime.now()
        instance.user_entity.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'stir',
                  'company_name',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar',
                  'position', ]


class UserEntityServicePersonalDataSerializer(serializers.ModelSerializer):
    stir = serializers.CharField(source='user_entity.stir')
    company_name = serializers.CharField(source='user_entity.company_name')
    position = serializers.CharField(source='user_entity.position')
    description = serializers.CharField(source='user_entity.description')
    service_certificate = serializers.FileField(source='user_entity.service_certificate')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    def update(self, instance, validated_data):
        instance.user_entity.position = validated_data.get('user_entity').get('position', instance.user_entity.position)
        instance.user_entity.stir = validated_data.get('user_entity').get('stir', instance.user_entity.stir)
        instance.user_entity.company_name = validated_data.get('user_entity').get('company_name',
                                                                                  instance.user_entity.company_name)
        instance.user_entity.service_certificate = validated_data.get('user_entity').get('service_certificate',
                                                                                         instance.user_entity.service_certificate)
        instance.user_entity.description = validated_data.get('user_entity').get('description',
                                                                                 instance.user_entity.description)
        instance.user_entity.updated_at = datetime.now()
        instance.user_entity.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'stir',
                  'company_name',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar',
                  'position',
                  'description',
                  'service_certificate', ]


class UserBuyerPersonalDataSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar', ]


class UserIndividualPersonalDataSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    service_certificate = serializers.FileField(source='user_individual.service_certificate')
    description = serializers.CharField(source='user_individual.description')

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar',
                  'service_certificate',
                  'description', ]


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id',
                  'subcategory',
                  'age',
                  'weight',
                  'amount',
                  'price',
                  'address',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo',
                  'user', ]


class PostCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['subcatalog',
                  'volume',
                  'amount',
                  'price',
                  'address',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo',
                  'user', ]


class PostServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['subservice',
                  'price',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo',
                  'service_type',
                  'user', ]
