from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from storage.views import FileViewSet, ShareFiles

router = SimpleRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    # path('', views.index),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('share/<slug:uuid>', ShareFiles.as_view(), name='share')


]
