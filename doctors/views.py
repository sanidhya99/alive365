from users.models import Appointments
from rest_framework.response import Response
from rest_framework import generics, status
from authentication.models import CustomUser
from .serializers import GetDoctorsSerializer,DoctorsCategorySerializer,FamousDoctorsSerializer,DoctorsSerializer,DoctorTimeSlotSerializer
from .models import DoctorCategory,Doctors
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import random
import requests
from rest_framework.permissions import AllowAny
from alive365.permissions import IsVerified
from users.serializers import DateWiseAppointmentSerializer
from twilio.rest import Client
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def send_otp(mobile, otp):
    """
    Send OTP via SMS.
    """
    url = f"https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/{mobile}/{otp}/Your 365 Alive OTP is"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, data=payload, headers=headers)
    if response.ok:
        return True
    else:
        return False

# def send_otp(mobile, otp):
#     account_sid = settings.OTP_SID
#     auth_token = settings.OTP_AUTH_TOKEN
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         from_=settings.OTP_NUMBER,  # Ensure this is correct
#         body=f'Hello! Your Alive 365 OTP is {otp}',  # Include the OTP dynamically
#         to=mobile  # Use the passed mobile number
#     )
#     print(message.sid)
#     return message.sid

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class DoctorsCategories(generics.ListCreateAPIView):
    serializer_class=DoctorsCategorySerializer
    permission_classes=[AllowAny]
    queryset=DoctorCategory.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit', None)
        
        if limit is not None:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass  # If limit is not an integer, ignore it and return the full queryset

        return queryset



class DoctorRegistration(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            name = request.data.get('name')
            number = request.data.get('phoneNumber')
            if not name or not number:
                return Response({"message": "Name and number are required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                doctor=Doctors.objects.get(phone=number)
                if doctor is not None:
                    return Response({"message":"User exists!"},status=200)

            except:
                doctor = Doctors.objects.create(name=name, phone=number)
                doctor.otp = random.randint(1000, 9999)
                doctor.save()
                token = get_tokens(doctor)
                check = send_otp(number, doctor.otp)
                if check:
                    return Response({"message": "OTP generated successfully", "token": token,"status":201}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "OTP not generated", "token": token,"status":400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "OTP not generated", "error": str(e),"status":400}, status=status.HTTP_400_BAD_REQUEST)

class DoctorLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            number = request.data.get('number')
            if not number:
                return Response({"message": "Number is required"}, status=status.HTTP_400_BAD_REQUEST)

            doctor = Doctors.objects.get(phone=number)
            doctor.otp = random.randint(1000, 9999)
            doctor.save()
            token = get_tokens(doctor)
            check = send_otp(number, doctor.otp)
            if check:
                return Response({"message": "OTP generated successfully", "token": token}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "OTP not generated", "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "No user found with these credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "OTP not generated", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyDoctorOTPView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
        otp = request.data.get('otp')
        # print(f"user:{user}")
        if otp is None:
            return Response({"message": "OTP is required"}, status=400)

        try:
            if user.otp == otp:
                user.otp_verified=True
                user.save()
                image=user.picture
                category=user.category
                if category:
                    cat_name=DoctorCategory.objects.get(id=category).name
                    cat_icon=DoctorCategory.objects.get(id=category).icon
                    cat_id=DoctorCategory.objects.get(id=category).id
                    return Response({"message": "Authenticated Successfully","id":user.id,"name":user.name,"location":user.location,"image":image,"category":{"id":cat_id,"name":cat_name,"icon":cat_icon}}, status=200)
                else:    
                    return Response({"message": "Authenticated Successfully","id":user.id,"name":user.name,"location":user.location,"image":image,"category":"NULL"}, status=200)
            else:
                return Response({"message": "Authentication failed"}, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
        


class GetFamousDoctors(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FamousDoctorsSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        queryset = Doctors.objects.all()

        if location:
            queryset = queryset.filter(location=location)

        return queryset.order_by('-rating')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': 'Data fetched successfully!',
                'data': serializer.data,
                'status': 200,
                'status_text': 'ok'
            }, status=200)
        except Exception as e:
            return Response({
                'message': 'Error!',
                'error': str(e),
                'status': 400,
                'status_text': 'error'
            }, status=400)
        
class GetDoctors(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FamousDoctorsSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        category = self.request.query_params.get('category', None)
        queryset = Doctors.objects.all()

        if location:
            queryset = queryset.filter(location=location)
        if category:
            category=DoctorCategory.objects.get(name=category)
            queryset = queryset.filter(category=category)

        return queryset.order_by('-rating')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': 'Data fetched successfully!',
                'data': serializer.data,
                'status': 200,
                'status_text': 'ok'
            }, status=200)
        except Exception as e:
            return Response({
                'message': 'Error!',
                'error': str(e),
                'status': 400,
                'status_text': 'error'
            }, status=400)
class GetDateWiseAppointments(generics.ListAPIView):        
    permission_classes=[IsVerified]
    serializer_class=DateWiseAppointmentSerializer

    def get_queryset(self):
        queryset=Appointments.objects.all()
        doctor=self.request.query_params.get('doctor', None)
        date=self.request.query_params.get('date', None)

        if doctor:
            queryset=queryset.filter(doctor=doctor)
        if date:
            queryset=queryset.filter(date=date)
        return queryset.order_by('time_slot')
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': 'Data fetched successfully!',
                'data': serializer.data,
                'status': 200,
                'status_text': 'ok'
            }, status=200)
        except Exception as e:
            return Response({
                'message': 'Error!',
                'error': str(e),
                'status': 400,
                'status_text': 'error'
            }, status=400)
        


class DoctorTimeSlotView(generics.ListAPIView):
    serializer_class = DoctorTimeSlotSerializer

    def get_queryset(self):
        # Extract the doctor ID from query parameters
        doctor_id = self.request.query_params.get('doctor')
        
        if doctor_id:
            return Doctors.objects.filter(id=doctor_id)
        return Doctors.objects.none()        
    
class EditDoctor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=DoctorsSerializer
    permission_classes=[IsVerified]
    queryset=Doctors.objects.all()
    lookup_field='id'

class GetDoctor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=GetDoctorsSerializer
    permission_classes=[AllowAny]
    queryset=Doctors.objects.all()
    lookup_field='id'

class GetAnalytics(generics.ListAPIView):
    permission_classes = [IsVerified]

    def get_queryset(self):
        mode = self.request.query_params.get('mode', None)
        time = self.request.query_params.get('time', None)
        pay = self.request.query_params.get('payment', None)
        queryset = Appointments.objects.filter(doctor=self.request.user)

        # Mode filtering
        if mode:
            if mode == 'online':
                queryset = queryset.filter(mode=True)
            elif mode == 'offline':
                queryset = queryset.filter(mode=False)
        if pay:
            if pay == 'online':
                queryset = queryset.filter(paid=True)
            elif pay == 'offline':
                queryset = queryset.filter(paid=False)
        
        # Time filtering
        if time:
            current_time = timezone.now().date()  # Get current date
            if time == 'week':
                time_threshold = current_time - timedelta(weeks=1)
            elif time == 'half':
                time_threshold = current_time - relativedelta(months=6)  # Subtract 6 months
            elif time == 'month':
                time_threshold = current_time - relativedelta(months=1)
            elif time == 'year':
                time_threshold = current_time - relativedelta(years=1)
            
            queryset = queryset.filter(date__gte=time_threshold)

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            count = queryset.count()
            return Response({
                'message': 'Data fetched successfully!',
                'count': count,
                'status': 200,
                'status_text': 'ok'
            }, status=200)
        except Exception as e:
            return Response({
                'message': 'Error!',
                'error': str(e),
                'status': 400,
                'status_text': 'error'
            }, status=400)