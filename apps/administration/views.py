from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.administration.serializer import UserAdminSerializer, UserAdminRetrieveSerializer, UserAdminRolesSerializer
from apps.authentication.models import User


class UserAdminModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return UserAdminRetrieveSerializer(args[0])
        return super().get_serializer(*args, **kwargs)


class UserAdminRolesListAPIView(ListAPIView):
    queryset = Group.objects.filter(role='ADMIN')
    serializer_class = UserAdminRolesSerializer
