from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid
import random


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
    


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=4)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def generate_otp(self):
        self.otp = f"{random.randint(1000, 9999)}"



class UploadedFile(models.Model):
    reaccel_id = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    class_names = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(default=timezone.now)
    epoch_value= models.IntegerField()
    batch_size= models.IntegerField()
    learning_rate= models.FloatField()
    project_status=models.IntegerField()
    model_type=models.IntegerField()

class login_at(models.Model):
    email=models.EmailField()
    user_name=models.CharField(max_length=100)
    reaccel_id=models.CharField(max_length=100)
    login_at=models.DateTimeField(default=timezone.now)