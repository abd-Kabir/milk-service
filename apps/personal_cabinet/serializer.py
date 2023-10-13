from rest_framework import serializers

from apps.authentication.models import User


class UserEntityPersonalDataSerializer(serializers.ModelSerializer):
    stir = serializers.CharField(source='user_entity.stir')
    company_name = serializers.CharField(source='user_entity.company_name')
    position = serializers.CharField(source='user_entity.position')
    gender_display = serializers.CharField(source='get_gender_display')

    class Meta:
        model = User
        fields = ['id',
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


class UserIndividualPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'last_name',
                  'phone_number',
                  'email',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar', ]


class UserBuyerPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'last_name',
                  'phone_number',
                  'email',
                  'address',
                  'gender',
                  'gender_display',
                  'birthday',
                  'avatar', ]
