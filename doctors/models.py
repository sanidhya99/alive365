from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from authentication.models import CustomUser

# Create your models here.
class DoctorCategory(models.Model):
    name=models.CharField(max_length=50) 
    doctors=models.ManyToManyField('Doctors', related_name='categories')
    def __str__(self):
        return self.name

class Doctors(CustomUser):
    category=models.ForeignKey(DoctorCategory, related_name="doctor_category", on_delete=models.CASCADE)
    experience = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])  # Adjust the minimum value as needed
    qualification = models.CharField(max_length=4,default="MBBS")
    qualification_doc = models.CharField(max_length=10000,default="MBBS",blank=True,null=True)
    identity_doc = models.CharField(max_length=10000,default="MBBS",blank=True,null=True)
    price=models.IntegerField()
    rating=models.IntegerField(default=0)
    rating_no=models.IntegerChoices(default=0)
    time_slot=ArrayField(ArrayField(models.TimeField(),size=2,default=list),blank=True,null=True,default=list)
    def __str__(self):
        return self.name