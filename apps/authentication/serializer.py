from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.models import User, UserLegalEntity, UserIndividual, UserAdmin
from apps.tools.models import Region, District, CompanyType
from config.utils.api_exceptions import APIValidation


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
    middle_name = serializers.CharField(required=False)
    first_name = serializers.CharField()
    position = serializers.CharField(required=False)
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


class UserAdminRetrieveSerializer(serializers.ModelSerializer):
    position = serializers.CharField(allow_null=True, source='user_admin.position')
    group = serializers.IntegerField(allow_null=True, source='groups.first.id')

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'last_name',
                  'first_name',
                  'phone_number',
                  'email',
                  'position',
                  'group', ]


class UserAdminSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    last_name = serializers.CharField()
    first_name = serializers.CharField()

    phone_number = serializers.CharField()
    email = serializers.EmailField()
    position = serializers.CharField(required=False)
    group = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Group.objects.filter(role='ADMIN'))

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email')
        position = validated_data.get('position', None)
        group = validated_data.get('group')
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            phone_number=phone_number,
                                            email=email)
            user.groups.add(group)
            UserAdmin.objects.create(position=position,
                                     user=user)
        except:
            raise APIValidation("User with this username, email or phone number already exists!",
                                status_code=status.HTTP_400_BAD_REQUEST)
        return user

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.username)
        password = validated_data.get('password')

        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)

        phone_number = validated_data.get('phone_number', instance.phone_number)
        email = validated_data.get('email', instance.email)
        position = validated_data.get('position', instance.user_admin.position)
        group = validated_data.get('group', instance.groups.first())
        try:
            instance.username = username
            if password:
                instance.set_password(password)
            instance.first_name = first_name
            instance.last_name = last_name
            instance.phone_number = phone_number
            instance.email = email
            instance.groups.clear()
            instance.groups.add(group)

            instance.user_admin.position = position
            instance.save()
            instance.user_admin.save()
        except:
            raise APIValidation("Bad request", status_code=status.HTTP_400_BAD_REQUEST)
        return instance


class UserAdminRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id',
                  'name']
