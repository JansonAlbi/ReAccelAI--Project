from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class User_info(models.Model):
    reaccelai_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email
    


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = 'file_upload'  # Add this line to specify the app_label
