from django.urls import path, re_path, include

urlpatterns = [
    # path('', views.index),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
