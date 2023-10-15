from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.models import User, UserLegalEntity, UserIndividual
from apps.tools.models import Region, District, CompanyType
from config.utils.api_exceptions import APIValidation


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_type = None
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        group = user.groups.all()
        if group:
            group = group.first()
            token['group'] = group.name
            if hasattr(user, 'user_entity'):
                user_type = user.user_entity
            elif hasattr(user, 'user_individual'):
                user_type = user.user_individual
            if user_type:
                token['subservice'] = list(
                    user_type.subservice.values('id', 'name_uz', 'name_ru', 'name_en', 'service',
                                                'service__name_uz', 'service__name_ru', 'service__name_en'))
                token['subcatalog'] = list(
                    user_type.subcatalog.values('id', 'name_uz', 'name_ru', 'name_en', 'catalog',
                                                'catalog__name_uz', 'catalog__name_ru', 'catalog__name_en'))
                token['subcategory'] = list(
                    user_type.subcategory.values('id', 'name_uz', 'name_ru', 'name_en', 'category',
                                                 'category__name_uz', 'category__name_ru', 'category__name_en'))

        return token


class BuyerSignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    first_name = serializers.CharField()
    group = serializers.CharField()

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        middle_name = validated_data.get('middle_name')
        group_name = validated_data.get('group').upper()
        group = Group.objects.get(name=group_name)
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   is_active=False)
        user.groups.add(group)
        return user


class BuyerSignUpFinalSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    region = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=District.objects.all())

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        region = validated_data.get('region')
        district = validated_data.get('district')

        user = get_object_or_404(User, username=username)
        user.set_password(password)
        user.save()

        user.user_buyer.region = region
        user.user_buyer.district = district
        user.user_buyer.save()
        return user


class SignUpPersonalDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    first_name = serializers.CharField()
    position = serializers.CharField(required=False)
    user_type = serializers.CharField(required=False)
    group = serializers.CharField()

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        middle_name = validated_data.get('middle_name')
        position = validated_data.get('position')
        user_type = validated_data.get('user_type', '').lower()
        group_name = validated_data.get('group').upper()
        group = Group.objects.get(name=group_name)
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   is_active=False)
        user.groups.add(group)
        if user_type == 'entity':
            UserLegalEntity.objects.create(position=position,
                                           user=user)
        elif user_type == 'individual':
            UserIndividual.objects.create(user=user)

        return user


class SignUpIndividualAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    region = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=District.objects.all())

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        region = validated_data.get('region')
        district = validated_data.get('district')

        user = get_object_or_404(User, username=username)
        user.set_password(password)
        user.save()

        user.user_individual.region = region
        user.user_individual.district = district
        user.user_individual.save()
        return user


class SignUpEntityAuthSerializer(serializers.Serializer):
    stir = serializers.CharField(required=True, write_only=True)
    company_name = serializers.CharField(required=True, write_only=True)
    company_description = serializers.CharField(required=True, write_only=True)
    company_type = serializers.PrimaryKeyRelatedField(required=True, write_only=True,
                                                      queryset=CompanyType.objects.all())

    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    region = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=District.objects.all())

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        stir = validated_data.get('stir')
        company_name = validated_data.get('company_name')
        company_description = validated_data.get('company_description')
        company_type = validated_data.get('company_type')
        region = validated_data.get('region')
        district = validated_data.get('district')

        user = get_object_or_404(User, username=username)
        user.set_password(password)
        user.save()

        user.user_entity.stir = stir
        user.user_entity.company_name = company_name
        user.user_entity.company_description = company_description
        user.user_entity.company_type = company_type
        user.user_entity.region = region
        user.user_entity.district = district
        user.user_entity.save()
        return user
