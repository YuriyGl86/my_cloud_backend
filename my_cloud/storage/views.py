import mimetypes
import logging

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from storage.models import UploadFiles
from storage.permisions import IsOwnerOrAdmin
from storage.serializers import FileSerializer

logger = logging.getLogger("main")


# Create your views here.
class FileViewSet(viewsets.ModelViewSet):
    queryset = UploadFiles.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        comment = self.request.POST.get('comment', None)
        rename = self.request.POST.get('rename', None)
        filename = rename if rename else file.name
        logger.info(f"Загрузка файла. Имя файла: {file.name}, переименование: {rename}, коммент: {comment}")
        serializer.save(name=filename, size=file.size, owner=self.request.user, comment=comment)

    def get_queryset(self):
        user = self.request.user
        requested_user_id = self.request.query_params.get('id', None)
        if requested_user_id:
            return UploadFiles.objects.filter(owner=requested_user_id).order_by('id')
        return UploadFiles.objects.filter(owner=user).order_by('id')

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(UploadFiles, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        return super().get_permissions()

    def perform_update(self, serializer):
        name = self.request.data.get('name', None)
        args = {}
        if name:
            args['name'] = name
        serializer.save(**args)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        file_type = mimetypes.guess_type(obj.name)[0]
        content_type = file_type if file_type else "application/octet-stream"
        # response = HttpResponse(obj.file.file, content_type=content_type)
        # response['Content-Disposition'] = 'attachment; filename=' + obj.name
        # response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response = FileResponse(obj.file.file, as_attachment=True, content_type=content_type, filename =obj.name )
        logger.info(f"Скачивание файла по кнопке. name = {obj.name} ,file_type = {content_type} ")
        obj.last_download = now()
        obj.save()

        return response


class ShareFiles(generics.RetrieveAPIView):
    queryset = UploadFiles.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        file_type = mimetypes.guess_type(obj.name)[0]
        response = HttpResponse(obj.file.file, content_type=file_type if file_type else "application/octet-stream")
        response['Content-Disposition'] = 'inline;filename=' + obj.name
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        logger.info(f"Скачивание файла по ссылке.")
        obj.last_download = now()
        obj.save()
        return response
