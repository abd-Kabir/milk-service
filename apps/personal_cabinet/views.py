from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory, PostCatalog, PostService
from apps.personal_cabinet.serializer import UserEntityPersonalDataSerializer, UserEntityServicePersonalDataSerializer, \
    UserBuyerPersonalDataSerializer, UserIndividualPersonalDataSerializer, PostCategorySerializer, \
    PostCatalogSerializer, PostServiceSerializer, CombinedPostSerializer
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

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404("User not found")


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

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404("User not found")


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
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return PostCategory.objects.filter(user=self.request.user)


class PostCatalogModelViewSet(ModelViewSet):
    queryset = PostCatalog.objects.all()
    serializer_class = PostCatalogSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return PostCatalog.objects.filter(user=self.request.user)


class PostServiceModelViewSet(ModelViewSet):
    queryset = PostService.objects.all()
    serializer_class = PostServiceSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return PostService.objects.filter(user=self.request.user)


class CombinedPostAPIView(ListAPIView):
    serializer_class = CombinedPostSerializer

    def get_queryset(self):
        post_category = PostCategory.objects.all()
        post_catalog = PostCatalog.objects.all()
        post_service = PostService.objects.all()

        # Combine the data from the three models into a dictionary
        combined_data = {
            "model_a_data": post_category,
            "model_b_data": post_catalog,
            "model_c_data": post_service,
        }

        return [combined_data]
