from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
# Create your models here.

class Designation(models.Model):
    emp_designation = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.emp_designation


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=20,blank=True,null=True)
    USERNAME_FIELD = 'email'  # Use email instead of username
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    