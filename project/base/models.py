from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
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
    


class Login_history(models.Model):
    user_info = models.ForeignKey(User_info, on_delete=models.CASCADE)
    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
