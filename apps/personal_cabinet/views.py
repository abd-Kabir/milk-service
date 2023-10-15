from random import shuffle

from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import User
from apps.personal_cabinet.models import PostCategory, PostCatalog, PostService, Application
from apps.personal_cabinet.serializer import UserEntityPersonalDataSerializer, UserEntityServicePersonalDataSerializer, \
    UserBuyerPersonalDataSerializer, UserIndividualPersonalDataSerializer, PostCategorySerializer, \
    PostCatalogSerializer, PostServiceSerializer, PostCategoryCombineSerializer, PostCatalogCombineSerializer, \
    PostServiceCombineSerializer, ApplicationCreateSerializer, ApplicationListSerializer
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
                return UserEntityServicePersonalDataSerializer(args[0], context={"request": self.request})
            return UserEntityPersonalDataSerializer(args[0], context={"request": self.request})
        elif hasattr(user, 'user_individual'):
            if is_service:
                return UserEntityServicePersonalDataSerializer(args[0], context={"request": self.request})
            return UserIndividualPersonalDataSerializer(args[0], context={"request": self.request})
        elif hasattr(user, 'user_buyer'):
            return UserBuyerPersonalDataSerializer(args[0], context={"request": self.request})
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


# class GetInterestsAPIView(APIView):
#     def get(self, request):
#         user = request.user
#         user_type = None
#         if hasattr(user, 'user_entity'):
#             user_type = user.user_entity
#         elif hasattr(user, 'user_individual'):
#             user_type = user.user_individual
#         subservice = list(user_type.subservice.values('id', 'name_uz', 'name_ru', 'name_en'))
#         subcatalog = list(user_type.subcatalog.values('id', 'name_uz', 'name_ru', 'name_en'))
#         subcategory = list(user_type.subcategory.values('id', 'name_uz', 'name_ru', 'name_en'))
#         return Response({
#             "subservice": subservice,
#             "subcatalog": subcatalog,
#             "subcategory": subcategory
#         })


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


class CombinedPostAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        types = request.query_params.get('type')

        limit = int(request.query_params.get('limit', 12))
        offset = int(request.query_params.get('offset', 0))

        queryset_category = PostCategory.objects.all()
        serializer_category = PostCategoryCombineSerializer(queryset_category, many=True,
                                                            context={'request': self.request})
        category_data = serializer_category.data
        category_data = [{**item, 'post_type': 'CATEGORY'} for item in category_data]

        queryset_catalog = PostCatalog.objects.all()
        serializer_catalog = PostCatalogCombineSerializer(queryset_catalog, many=True,
                                                          context={'request': self.request})
        catalog_data = serializer_catalog.data
        catalog_data = [{**item, 'post_type': 'CATALOG'} for item in catalog_data]

        queryset_service = PostService.objects.all()
        serializer_service = PostServiceCombineSerializer(queryset_service, many=True,
                                                          context={'request': self.request})
        service_data = serializer_service.data
        service_data = [{**item, 'post_type': 'SERVICE'} for item in service_data]
        if types:
            types = types.split(',')
            result = []
            if 'category' in types:
                result.extend(category_data)
            if 'catalog' in types:
                result.extend(catalog_data)
            if 'service' in types:
                result.extend(service_data)
            result = result[offset:offset + limit]
            shuffle(result)
        else:
            result = category_data + catalog_data + service_data
        return Response(result)


class CombinedPostRetrieve(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        post_type = request.query_params.get('post_type', None)
        if not post_type:
            raise APIValidation("post_type was not included")
        match post_type:
            case 'CATEGORY':
                instance = get_object_or_404(PostCategory, pk=pk)
                serializer = PostCategoryCombineSerializer(instance, context={'request': self.request})

            case 'CATALOG':
                instance = get_object_or_404(PostCatalog, pk=pk)
                serializer = PostCatalogCombineSerializer(instance, context={'request': self.request})

            case 'SERVICE':
                instance = get_object_or_404(PostService, pk=pk)
                serializer = PostServiceCombineSerializer(instance, context={'request': self.request})
        return Response(serializer.data)


class ApplicationCreateAPIView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer


class ApplicationListAPIView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer


class ApplicationApply(APIView):
    def post(self, request, pk):
        user = request.user
        user_category_posts = user.post_category.values_list('id', flat=True)
        user_catalog_posts = user.post_catalog.values_list('id', flat=True)
        user_service_posts = user.post_service.values_list('id', flat=True)
        user_posts = list(user_category_posts) + list(user_catalog_posts) + list(user_service_posts)
        if not (pk in user_posts):
            raise APIValidation("Application with this id doesn't belongs you",
                                status_code=status.HTTP_400_BAD_REQUEST)

        app_status = 'ACCEPTED'
        zoom_link = request.data.get('zoom_link')
        zoom_time = request.data.get('zoom_time')

        instance = get_object_or_404(Application, pk=pk)
        if instance.app_type == 'ZOOM':
            instance.zoom_link = zoom_link
            instance.zoom_time = zoom_time
            instance.status = app_status
            instance.save()
            return Response({
                "id": instance.id,
                "created_at": instance.created_at,
                "status": instance.status,
                "phone_number": instance.phone_number,
                "zoom_link": instance.zoom_link,
                "zoom_time": instance.zoom_time
            })
        return Response({
            "id": instance.id,
            "created_at": instance.created_at,
            "status": instance.status,
            "phone_number": instance.phone_number
        })
