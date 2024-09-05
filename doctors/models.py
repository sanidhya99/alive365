from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from authentication.models import CustomUser

# Create your models here.
class DoctorCategory(models.Model):
    name=models.CharField(max_length=50) 
    icon=models.CharField(max_length=10000,default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkoyUQaux4PEUmEPGc7PodeN8XbgC4aOBsug&s")
    doctors=models.ManyToManyField('Doctors', related_name='categories')
    def __str__(self):
        return self.name

class Doctors(CustomUser):
    category=models.ForeignKey(DoctorCategory, related_name="doctor_category", on_delete=models.CASCADE,null=True,blank=True)
    picture=models.CharField(max_length=10000,blank=True,null=True)
    experience = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])  # Adjust the minimum value as needed
    qualification = models.CharField(max_length=4,default="MBBS",null=True,blank=True)
    qualification_doc = models.CharField(max_length=10000,default="MBBS",blank=True,null=True)
    identity_doc = models.CharField(max_length=10000,default="MBBS",blank=True,null=True)
    price=models.IntegerField(null=True,blank=True)
    rating=models.IntegerField(default=0)
    rating_no=models.IntegerField(default=0)
    time_slot=ArrayField(ArrayField(models.TimeField(),size=2,default=list),blank=True,null=True,default=list)
    bio=models.CharField(max_length=10000,null=True,blank=True)
    def __str__(self):
        return self.name