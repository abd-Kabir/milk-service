from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory, PostCatalog, PostService
from apps.personal_cabinet.serializer import UserEntityPersonalDataSerializer, UserEntityServicePersonalDataSerializer, \
    UserBuyerPersonalDataSerializer, UserIndividualPersonalDataSerializer, PostCategorySerializer, \
    PostCatalogSerializer, PostServiceSerializer
from config.utils.api_exceptions import APIValidation


class PersonalDataRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        groups = user.groups.all()
        is_service = False
        if groups:
            group = groups.first()
            if group.name == 'SERVICE':
                is_service = True
        if hasattr(user, 'user_entity'):
            if is_service:
                return UserEntityServicePersonalDataSerializer(args[0])
            return UserEntityPersonalDataSerializer(args[0])
        elif hasattr(user, 'user_individual'):
            if is_service:
                return UserEntityServicePersonalDataSerializer(args[0])
            return UserIndividualPersonalDataSerializer(args[0])
        elif hasattr(user, 'user_buyer'):
            return UserBuyerPersonalDataSerializer(args[0])
        else:
            raise APIValidation("Bad request", status_code=status.HTTP_400_BAD_REQUEST)


class PersonalDataUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        groups = user.groups.all()
        is_service = False
        if groups:
            group = groups.first()
            if group.name == 'SERVICE':
                is_service = True
        if hasattr(user, 'user_entity'):
            if is_service:
                return UserEntityServicePersonalDataSerializer(args[0], data=kwargs['data'], partial=True)
            return UserEntityPersonalDataSerializer(args[0], data=kwargs['data'], partial=True)
        elif hasattr(user, 'user_individual'):
            if is_service:
                return UserEntityServicePersonalDataSerializer(args[0], data=kwargs['data'], partial=True)
            return UserIndividualPersonalDataSerializer(args[0], data=kwargs['data'], partial=True)
        elif hasattr(user, 'user_buyer'):
            return UserBuyerPersonalDataSerializer(args[0], data=kwargs['data'], partial=True)
        else:
            raise APIValidation("Bad request", status_code=status.HTTP_400_BAD_REQUEST)


class GetInterestsAPIView(APIView):
    def get(self, request):
        user = request.user
        user_type = None
        if hasattr(user, 'user_entity'):
            user_type = user.user_entity
        elif hasattr(user, 'user_individual'):
            user_type = user.user_individual
        subservice = list(user_type.subservice.values('id', 'name_uz', 'name_ru', 'name_en'))
        subcatalog = list(user_type.subcatalog.values('id', 'name_uz', 'name_ru', 'name_en'))
        subcategory = list(user_type.subcategory.values('id', 'name_uz', 'name_ru', 'name_en'))
        return Response({
            "subservice": subservice,
            "subcatalog": subcatalog,
            "subcategory": subcategory
        })


class PostCategoryModelViewSet(ModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostCatalogModelViewSet(ModelViewSet):
    queryset = PostCatalog.objects.all()
    serializer_class = PostCatalogSerializer


class PostServiceModelViewSet(ModelViewSet):
    queryset = PostService.objects.all()
    serializer_class = PostServiceSerializer