from django.urls import path
app_name = 'auth'

urlpatterns = [
    path('api/token/', JWTObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
