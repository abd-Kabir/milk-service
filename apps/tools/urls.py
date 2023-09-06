from django.urls import path

from apps.tools.views import RegionListAPIView, DistrictListAPIView, CompanyTypeListAPIView

app_name = 'tools'
urlpatterns = [
    path('region/', RegionListAPIView.as_view(), name='region'),
    path('district/<int:pk>/', DistrictListAPIView.as_view(), name='district'),
    path('company-type/', CompanyTypeListAPIView.as_view(), name='company_types'),
]
