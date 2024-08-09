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
    time_slot=models.TimeField()
    def __str__(self):
        return self.patient.name