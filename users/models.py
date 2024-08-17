from django.db import models
from doctors.models import *
from authentication.models import CustomUser
class Appointments(models.Model):
    doctor=models.ForeignKey(Doctors, related_name="appointment_doctor", on_delete=models.CASCADE)
    patient=models.ForeignKey(CustomUser, related_name="appointment_user", on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    description=models.CharField(max_length=100)
    address=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField(blank=True,null=True)
    time_slot=models.TimeField()
    def __str__(self):
        return self.patient.name
    
class UserOffers(models.Model):
    image=models.CharField(max_length=1000)    
