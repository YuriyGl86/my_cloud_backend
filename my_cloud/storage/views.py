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
        serializer.save(name=file.name, size=file.size, owner=self.request.user)
