from datetime import datetime

from rest_framework import serializers

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory, PostCatalog, PostService
from config.utils.api_exceptions import APIValidation


class UserEntityPersonalDataSerializer(serializers.ModelSerializer):
    stir = serializers.CharField(source='user_entity.stir')
    company_name = serializers.CharField(source='user_entity.company_name')
    position = serializers.CharField(source='user_entity.position')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    def update(self, instance, validated_data):
        instance_user_entity = instance.user_entity
        user_entity = validated_data.get('user_entity')
        if user_entity:
            instance_user_entity.position = user_entity.get('position', instance_user_entity.position)
            instance_user_entity.company_name = user_entity.get('company_name', instance_user_entity.company_name)
            instance_user_entity.position = user_entity.get('position', instance_user_entity.position)
            instance_user_entity.updated_at = datetime.now()
            instance_user_entity.save()
            validated_data.pop('user_entity')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, value):
        user = value
        user_type = None
        if hasattr(user, 'user_entity'):
            user_type = user.user_entity
        elif hasattr(user, 'user_individual'):
            user_type = user.user_individual
        interested_subcategories = user_type.subcategory.values_list('id', flat=True)
        subcategory = int(self.context['request'].data.get('subcategory'))
        if subcategory in interested_subcategories:
            return user
        raise APIValidation("You are choosing wrong Category")

    class Meta:
        model = PostCategory
        fields = ['id',
                  'category',
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, value):
        user = value
        user_type = None
        if hasattr(user, 'user_entity'):
            user_type = user.user_entity
        elif hasattr(user, 'user_individual'):
            user_type = user.user_individual
        interested_subcatalogs = user_type.subcatalog.values_list('id', flat=True)
        subcatalog = int(self.context['request'].data.get('subcatalog'))
        if subcatalog in interested_subcatalogs:
            return user
        raise APIValidation("You are choosing wrong Catalog")

    class Meta:
        model = PostCatalog
        fields = ['id',
                  'catalog',
                  'subcatalog',
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, value):
        user = value
        user_type = None
        if hasattr(user, 'user_entity'):
            user_type = user.user_entity
        elif hasattr(user, 'user_individual'):
            user_type = user.user_individual
        interested_subservices = user_type.subservice.values_list('id', flat=True)
        subcatalog = int(self.context['request'].data.get('subcatalog'))
        if subcatalog in interested_subservices:
            return user
        raise APIValidation("You are choosing wrong Service")

    class Meta:
        model = PostService
        fields = ['id',
                  'service',
                  'subservice',
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


class CombinedPostSerializer(serializers.Serializer):
    category = PostCategorySerializer(many=True)
    catalog = PostCatalogSerializer(many=True)
    service = PostServiceSerializer(many=True)
