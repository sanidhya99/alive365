from django.db import models
from .manage import *
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    username=None
    name=models.CharField(max_length=50)
    phone = models.CharField(max_length=10,unique=True, blank=True, null=True, validators=[RegexValidator(regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    email=models.EmailField(null=True,blank=True,unique=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    dob = models.DateField(null=True, blank=True)
    blood_group=models.CharField(max_length=5,blank=True,null=True)
    marital_status=models.BooleanField(default=False)
    height=models.FloatField(blank=True,null=True)
    weight=models.FloatField(blank=True,null=True)
    emergency_contact=models.CharField(max_length=10,blank=True,null=True)
    location=models.CharField(max_length=50,blank=True,null=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_verified=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects=CustomUserManager()
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
    REQUIRED_FIELDS=["name"]
    USERNAME_FIELD='phone'
    def __str__(self):
        return self.email