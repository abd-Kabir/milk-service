from django.contrib.auth.models import Group
from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.administration.serializer import UserAdminSerializer, UserAdminGetSerializer, UserAdminRolesSerializer
from apps.authentication.models import User


class UserAdminModelViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__role='ADMIN')
    serializer_class = UserAdminSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return UserAdminGetSerializer(args[0])
        elif self.action == 'list':
            return UserAdminGetSerializer(args[0], many=True)
        return super().get_serializer(*args, **kwargs)


class UserAdminRolesListAPIView(ListAPIView):
    queryset = Group.objects.filter(role='ADMIN')
    serializer_class = UserAdminRolesSerializer
