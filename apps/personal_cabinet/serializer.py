from datetime import datetime

from rest_framework import serializers, status

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory, PostCatalog, PostService, Application
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
        instance_user_entity = instance.user_entity
        user_entity = validated_data.get('user_entity')
        if user_entity:
            instance_user_entity.position = user_entity.get('position', instance_user_entity.position)
            instance_user_entity.stir = user_entity.get('stir', instance_user_entity.stir)
            instance_user_entity.company_name = user_entity.get('company_name', instance_user_entity.company_name)
            instance_user_entity.service_certificate = user_entity.get('service_certificate',
                                                                       instance_user_entity.service_certificate)
            instance_user_entity.description = user_entity.get('description', instance_user_entity.description)
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
                  'created_at',
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
                  'created_at',
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
                  'created_at',
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


class PostCategoryCombineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id',
                  'created_at',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo', ]


class PostCatalogCombineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCatalog
        fields = ['id',
                  'created_at',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo', ]


class PostServiceCombineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostService
        fields = ['id',
                  'created_at',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'photo', ]


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id',
                  'created_at',
                  'app_type',
                  'status',
                  'phone_number',
                  'buyer', ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_type = serializers.CharField(allow_null=True)

    def create(self, validated_data):
        app_type = validated_data.get('app_type')
        phone_number = validated_data.get('phone_number')
        buyer = validated_data.get('buyer')
        post_type = validated_data.get('post_type')

        post_category = validated_data.get('post_category')
        post_catalog = validated_data.get('post_catalog')
        post_service = validated_data.get('post_service')
        try:
            match post_type:
                case 'CATEGORY':
                    app = Application.objects.create(app_type=app_type,
                                                     phone_number=phone_number,
                                                     buyer=buyer,
                                                     post_category=post_category)
                case 'CATALOG':
                    app = Application.objects.create(app_type=app_type,
                                                     phone_number=phone_number,
                                                     buyer=buyer,
                                                     post_catalog=post_catalog)
                case 'SERVICE':
                    app = Application.objects.create(app_type=app_type,
                                                     phone_number=phone_number,
                                                     buyer=buyer,
                                                     post_service=post_service)
            return app
        except:
            raise APIValidation("post_type was not included", status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Application
        fields = ['post_category',
                  'post_catalog',
                  'post_service',
                  'app_type',
                  'phone_number',
                  'buyer',
                  'post_type', ]
