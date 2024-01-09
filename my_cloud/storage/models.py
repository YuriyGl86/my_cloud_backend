import uuid
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()
class UploadFiles(models.Model):
    file = models.FileField(upload_to='upload_files')
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4)
    size = models.BigIntegerField()

