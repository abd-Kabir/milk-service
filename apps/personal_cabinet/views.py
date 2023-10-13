from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import User
from apps.personal_cabinet.serializer import UserEntityPersonalDataSerializer, UserIndividualPersonalDataSerializer, \
    UserBuyerPersonalDataSerializer
from config.utils.api_exceptions import APIValidation


class PersonalDataModelViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if hasattr(user, 'user_entity'):
            return UserEntityPersonalDataSerializer(args[0])
        elif hasattr(user, 'user_individual'):
            return UserIndividualPersonalDataSerializer(args[0])
        elif hasattr(user, 'user_buyer'):
            return UserBuyerPersonalDataSerializer(args[0])
        else:
            raise APIValidation("Bad request", status_code=status.HTTP_400_BAD_REQUEST)
