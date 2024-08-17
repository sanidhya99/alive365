from rest_framework import serializers
from .models import *
from users.models import Appointments
from django.utils import timezone
from datetime import timedelta


class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = '__all__'

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class FamousDoctorsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    appointments_last_7_days = serializers.SerializerMethodField()

    class Meta:
        model = Doctors
        fields = ['name', 'category', 'rating', 'time_slot', 'appointments_last_7_days']

    def get_appointments_last_7_days(self, obj):
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        return Appointments.objects.filter(doctor=obj, date__range=[seven_days_ago, today]).count()