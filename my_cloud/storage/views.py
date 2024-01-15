import mimetypes

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from storage.models import UploadFiles
from storage.serializers import FileSerializer


# Create your views here.
class FileViewSet(viewsets.ModelViewSet):
    queryset = UploadFiles.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        comment = self.request.POST.get('comment', None)
        rename = self.request.POST.get('rename', None)
        filename = rename if rename else file.name
        serializer.save(name=filename, size=file.size, owner=self.request.user, comment=comment)

    def get_queryset(self):
        user = self.request.user
        requested_user_id = self.request.query_params.get('id', None)
        if requested_user_id and user.is_staff:
            return UploadFiles.objects.filter(owner=requested_user_id).order_by('id')
        return UploadFiles.objects.filter(owner=user).order_by('id')

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
        response = HttpResponse(obj.file.file, content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename=' + obj.name
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        obj.last_download=now()
        obj.save()
        return response


class ShareFiles(generics.RetrieveAPIView):
    queryset = UploadFiles.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'uuid'

    # def get_object(self):
    #     uuid=self.kwargs.get('uuid')
    #     obj = get_object_or_404(UploadFiles, uuid=uuid)
    #     return obj

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        typeobj=mimetypes.guess_type(obj.name)[0]
        print(typeobj)
        response = HttpResponse(obj.file.file, content_type=typeobj if typeobj else "application/octet-stream")
        response['Content-Disposition'] = 'inline;filename=' + obj.name
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        obj.last_download = now()
        obj.save()
        return response
