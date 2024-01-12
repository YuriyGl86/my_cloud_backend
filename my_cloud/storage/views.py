from django.shortcuts import render
from rest_framework import viewsets

from storage.models import UploadFiles
from storage.serializers import FileSerializer


# Create your views here.
class FileViewSet(viewsets.ModelViewSet):
    queryset = UploadFiles.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        comment = self.request.POST.get('comment', None)
        rename = self.request.POST.get('rename', None)
        filename = rename if rename else file.name
        serializer.save(name=filename, size=file.size, owner=self.request.user, comment=comment)

    def get_queryset(self):
        user = self.request.user
        id = self.request.query_params.get('id', None)
        if id and user.is_staff:
            return UploadFiles.objects.filter(owner=id).order_by('id')
        return UploadFiles.objects.filter(owner=user).order_by('id')

    def get_permissions(self):
        return super().get_permissions()

    def perform_update(self, serializer):
        name = self.request.data.get('name', None)

        args = {}
        if name:
            args['name'] = name

        serializer.save(**args)
