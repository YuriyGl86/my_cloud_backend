import uuid
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()
class UploadFiles(models.Model):
    file = models.FileField(upload_to='upload_files')
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    size = models.BigIntegerField()
    comment = models.CharField(max_length=256, blank=True, null=True)

