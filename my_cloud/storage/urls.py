from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from storage.views import FileViewSet

router = SimpleRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    # path('', views.index),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include(router.urls))
]
