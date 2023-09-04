from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.models import User, UserLegalEntity, UserIndividual


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

# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password2', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user
