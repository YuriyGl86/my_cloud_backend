from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from storage.views import FileViewSet, ShareFiles

router = SimpleRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    # path('', views.index),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include(router.urls)),
    path('api/v1/share/<slug:uuid>', ShareFiles.as_view(), name='share')


]
