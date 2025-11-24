from django.db import models

# Create your models here.
from django.contrib.auth.models import User

import random
import string
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    address=models.TextField()
    profile_pic=models.ImageField()
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    
    

class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))