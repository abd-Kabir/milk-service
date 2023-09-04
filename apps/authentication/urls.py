from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import JWTObtainPairView, SignUpPersonalDataAPIView, SignUpContactDataAPIView, \
    SignUpVerifyCodeAPIView

app_name = 'auth'

urlpatterns = [
    # sign in
    path('token/', JWTObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # sign up
    path('sign-up-personal/', SignUpPersonalDataAPIView.as_view(), name='sign_up_personal'),
    path('sign-up-contacts/<str:username>/', SignUpContactDataAPIView.as_view(), name='sign_up_contacts'),
    path('sign-up-verify/', SignUpVerifyCodeAPIView.as_view(), name='sign_up_verify'),
]
