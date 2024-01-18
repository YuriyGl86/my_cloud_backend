from django.urls import path

from my_cloud_main.views import MyCloudHome

urlpatterns = [
    path('', MyCloudHome.as_view(), name='home')
]