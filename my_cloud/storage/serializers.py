from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from storage.models import UploadFiles

UserModel = get_user_model()


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'email', 'first_name', 'is_staff']


class MyUserDeleteSerializer(serializers.Serializer):
    """
    Для настройки djoser в settings.py. Теперь djoser при удалении user по id не требует пароль.
    """
    pass


class MyUserSerializer(UserSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'is_staff']
        read_only_fields = ('username',)


class FileSerializer(ModelSerializer):
    class Meta:
        model = UploadFiles
        fields = ('owner', 'file', 'name', 'uploaded_at', 'last_download', 'uuid', 'size')
        read_only_fields = ['owner', 'name', 'uploaded_at', 'last_download', 'uuid', 'size']
