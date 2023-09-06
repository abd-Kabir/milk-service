from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.models import User, UserLegalEntity, UserIndividual
from apps.tools.models import Region, District, CompanyType


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token


class SignUpPersonalDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    first_name = serializers.CharField()
    position = serializers.CharField()
    user_type = serializers.CharField()

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        middle_name = validated_data.get('middle_name')
        position = validated_data.get('position')
        user_type = validated_data.get('user_type', '').lower()
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   is_active=False)
        if user_type == 'entity':
            UserLegalEntity.objects.create(position=position,
                                           user=user)
        elif user_type == 'individual':
            UserIndividual.objects.create(user=user)

        return user


class SignUpIndividualAuthSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    region = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=District.objects.all())

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.get('user')
        password = validated_data.get('password')
        region = validated_data.get('region')
        district = validated_data.get('district')

        user.set_password(password)
        user.is_active = True
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

    password = serializers.CharField(required=True, write_only=True)
    region = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(required=True, write_only=True, queryset=District.objects.all())

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.get('user')
        password = validated_data.get('password')

        stir = validated_data.get('stir')
        company_name = validated_data.get('company_name')
        company_description = validated_data.get('company_description')
        company_type = validated_data.get('company_type')
        region = validated_data.get('region')
        district = validated_data.get('district')

        user.set_password(password)
        user.is_active = True
        user.save()

        user.user_entity.stir = stir
        user.user_entity.company_name = company_name
        user.user_entity.company_description = company_description
        user.user_entity.company_type = company_type
        user.user_entity.region = region
        user.user_entity.district = district
        user.user_entity.save()
        return user
# test
