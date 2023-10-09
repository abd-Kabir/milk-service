from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.administration.models import Category, SubCategory
from apps.administration.serializer import UserAdminSerializer, UserAdminGetSerializer, UserAdminRolesSerializer, \
    CategorySerializer, CategoryListSerializer, SubCategorySerializer
from apps.authentication.models import User


class UserAdminModelViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__role='ADMIN').exclude(groups__name="SUPERADMIN")
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


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return CategoryListSerializer(args[0], many=True)
        return super().get_serializer(*args, **kwargs)


class SubCategoryModelViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
