from django.contrib.auth import get_user_model
from django.db.models import Sum
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from storage.models import UploadFiles

UserModel = get_user_model()


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'email', 'first_name', 'is_staff']


class MyUserDeleteSerializer(serializers.Serializer):
    """
    Для настройки djoser в settings.py. Теперь djoser при удалении user по id не требует пароль от этого user.
    """
    pass


class MyUserSerializer(UserSerializer):
    files_count = serializers.SerializerMethodField()
    files_size = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'first_name', 'is_staff', 'files_count', 'files_size']
        read_only_fields = ('username', 'id')

    def get_files_count(self, obj):
        return UploadFiles.objects.filter(owner=obj).count()

    def get_files_size(self, obj):
        return UploadFiles.objects.filter(owner=obj).aggregate(sum=Sum('size')).get('sum')


class FileSerializer(ModelSerializer):
    file_download_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadFiles
        fields = (
            'id', 'owner', 'file', 'name', 'uploaded_at', 'last_download', 'uuid', 'size', 'comment',
            'file_download_url')
        read_only_fields = ['id', 'owner', 'name', 'uploaded_at', 'last_download', 'uuid', 'size', 'file_download_url']

    def get_file_download_url(self, obj):
        return self.context['request'].build_absolute_uri(reverse('share', args=[str(obj.uuid)]))
