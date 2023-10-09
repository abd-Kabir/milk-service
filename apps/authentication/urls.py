from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import JWTObtainPairView, SignUpPersonalDataAPIView, SignUpContactDataAPIView, \
    SignUpVerifyCodeAPIView, SignUpAuthAPIView, SignUpInterestsAPIView, DeleteUserAPIView, VerifyPWAPIViewAPIView, \
    ChangePWAPIView, NewPWAPIView


app_name = 'auth'
urlpatterns = [
    # sign in
    path('token/', JWTObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # sign up
    path('sign-up-personal/', SignUpPersonalDataAPIView.as_view(), name='sign_up_personal'),
    path('sign-up-contacts/<str:username>/', SignUpContactDataAPIView.as_view(), name='sign_up_contacts'),
    path('sign-up-verify/', SignUpVerifyCodeAPIView.as_view(), name='sign_up_verify'),
    path('sign-up-auth/', SignUpAuthAPIView.as_view(), name='sign_up_auth'),
    path('sign-up-last/', SignUpInterestsAPIView.as_view(), name='sign_up_last'),

    # change-password
    path('change-pw/', ChangePWAPIView.as_view(), name='change_pw'),
    path('verify-pw/', VerifyPWAPIViewAPIView.as_view(), name='verify_pw'),
    path('upd-pw/', NewPWAPIView.as_view(), name='upd_pw'),

    # roles
    path('administration-roles/', UserAdminRolesListAPIView.as_view(), name='admin_roles'),

    path('delete-user/<str:username>/', DeleteUserAPIView.as_view(), name='delete_user'),
]

urlpatterns += router.urls
