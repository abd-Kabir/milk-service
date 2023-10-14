from django.contrib.auth.models import Group
from rest_framework import serializers, status

from apps.administration.models import UserAdministration, News, Banner
from apps.authentication.models import User
from config.utils.api_exceptions import APIValidation


# User-Admin
class UserAdminGetSerializer(serializers.ModelSerializer):
    position = serializers.CharField(allow_null=True, source='user_admin.position')
    group = serializers.IntegerField(allow_null=True, source='groups.first.id')
    group_display = serializers.CharField(allow_null=True, source='groups.first.name')

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'last_name',
                  'first_name',
                  'phone_number',
                  'email',
                  'position',
                  'group',
                  'group_display', ]


class UserAdminSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)

    last_name = serializers.CharField()
    first_name = serializers.CharField()

    phone_number = serializers.CharField()
    email = serializers.EmailField()
    position = serializers.CharField(required=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='groups')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email')
        position = validated_data.get('position', None)
        group = validated_data.get('groups')
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            phone_number=phone_number,
                                            email=email)
            user.groups.add(group)
            UserAdministration.objects.create(position=position,
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


# News
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id',
                  'created_at',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'photo', ]


# Banner
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id',
                  'created_at',
                  'title_uz',
                  'title_ru',
                  'title_en',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'photo', ]
