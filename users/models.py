from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from django.core.exceptions import ValidationError






# Create your models here.

class Designation(models.Model):
    emp_designation = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.emp_designation


class User(AbstractUser):
    username = None

    ADMIN = 'ADMIN'
    TL = 'TL'
    SR = 'SR'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TL, 'Team Leader'),
        (SR, 'Sales Representative'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=SR)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(max_length=20, blank=True, null=True)
    # designation = models.CharField(max_length=20,blank=True,null=True)
    is_accepted = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'  # Use email instead of username
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    






class Team(models.Model):
    team_name = models.CharField(max_length=255, unique=True)
    leader = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_team'
    )
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name='teams_as_member'
    )

    def clean(self):
        if self.leader and self.leader in self.members.all():
            raise ValidationError("Leader cannot be a member")

    def __str__(self):
        return self.team_name


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) # এটি আনকমেন্ট করুন
    teams = models.ManyToManyField(Team, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True) # এটি আনকমেন্ট করুন

    def __str__(self):
        return self.title



##########################################################