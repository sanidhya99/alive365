from rest_framework import serializers
from .models import *

class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = '__all__'