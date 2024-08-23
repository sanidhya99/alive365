from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import CustomUser
from rest_framework.permissions import BasePermission,AllowAny
from alive365.permissions import IsVerified
from doctors.models import Doctors
from .models import Appointments,UserOffers
from .serializers import AppointmentSerializer,FutureAppointmentDetailSerializer,UserOffersSerializer,PastAppointmentDetailSerializer
from django.utils import timezone

class UserLocation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,IsVerified]

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return Response({"message": "Not Authenticated"}, status=status.HTTP_403_FORBIDDEN)
        
        location = request.data.get('location')
        if not location:
            return Response({"message": "Location not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.location = location
        user.save()
        return Response({"message": "success", "location": user.location}, status=status.HTTP_200_OK)

class BookAppointment(generics.CreateAPIView):
    permission_classes=[IsVerified]
    def post(self, request, *args, **kwargs):
        mode=self.request.query_params.get('mode', None)
        if mode=="user":
            try:
                # Extract data from request
                doctor_pk = request.data.get("doctor")
                time_slot = request.data.get("time_slot")
                phone = request.data.get("phone")
                age = request.data.get("age")
                gender = request.data.get("gender")
                address = request.data.get("address")
                date = request.data.get("date")
                reason = request.data.get("reason")
                
            

                # Validate required fields
                if not doctor_pk or not time_slot:
                    return Response({'error': 'Doctor and time slot are required.'}, status=status.HTTP_400_BAD_REQUEST)

                # Retrieve doctor and patient objects
                try:
                    doctor = Doctors.objects.get(id=doctor_pk)
                except Doctors.DoesNotExist:
                    return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
                
                patient = CustomUser.objects.get(id=request.user.id)
                
                # Check for overlapping appointments
                if Appointments.objects.filter(doctor=doctor, time_slot=time_slot).exists():
                    return Response({'message': 'Time Slot Already Booked!','status':400,'status_text':"error"}, status=200)

                # Create appointment
                appointment = Appointments.objects.create(
                    doctor=doctor,
                    patient=patient,
                    phone=phone,
                    age=age,
                    date=date,
                    gender=gender,
                    address=address,
                    reason=reason,
                    time_slot=time_slot
                )
                appointment.save()

                # Return success response
                return Response({'message': 'Appointment booked successfully.','status':201,'status_text':'ok'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:

            try:
                # Extract data from request
                doctor_pk = request.data.get("doctor")
                patient_offline=request.data.get("patient_offline")
                time_slot = request.data.get("time_slot")
                phone = request.data.get("phone")
                age = request.data.get("age")
                gender = request.data.get("gender")
                address = request.data.get("address")
                date = request.data.get("date")
                reason = request.data.get("reason")
                
            

                # Validate required fields
                if not doctor_pk or not time_slot:
                    return Response({'error': 'Doctor and time slot are required.'}, status=status.HTTP_400_BAD_REQUEST)

                # Retrieve doctor and patient objects
                try:
                    doctor = Doctors.objects.get(id=doctor_pk)
                except Doctors.DoesNotExist:
                    return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
                
                # patient = CustomUser.objects.get(id=request.user.id)
                
                # Check for overlapping appointments
                if Appointments.objects.filter(doctor=doctor, time_slot=time_slot).exists():
                    return Response({'message': 'Time Slot Already Booked!','status':400,'status_text':"error"}, status=200)

                # Create appointment
                appointment = Appointments.objects.create(
                    doctor=doctor,
                    # patient=patient,
                    patient_offline=patient_offline,
                    phone=phone,
                    age=age,
                    date=date,
                    gender=gender,
                    address=address,
                    reason=reason,
                    time_slot=time_slot
                )
                appointment.save()

                # Return success response
                return Response({'message': 'Appointment booked successfully.','status':201,'status_text':'ok'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
        
class GetAppointments(generics.ListAPIView):
    permission_classes=[IsVerified]
    serializer_class=AppointmentSerializer
    def get_queryset(self):
        queryset = Appointments.objects.all()
        doctor_id = self.request.query_params.get('doctor', None)
        time_slot = self.request.query_params.get('time_slot', None)
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if time_slot:
            queryset = queryset.filter(time_slot=time_slot)

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'message':'Data fetched successfully!','data':serializer.data,'status':200,'status_text':'ok'},status=200)
        except Exception as e:
            return Response({'message':'Error!','error':e,'status':400,'status_text':'error'},status=200)

class GetFutureUserAppointments(generics.ListAPIView):
    permission_classes=[IsVerified]
    serializer_class=FutureAppointmentDetailSerializer
    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        return Appointments.objects.filter(patient=user, date__gte=today).order_by('date')

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
                'error': str(e),  # Return the error as a string
                'status': 400,
                'status_text': 'error'
            }, status=400)  # Return a 400 status code for errors
    
class GetUserOffers(generics.ListCreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=UserOffersSerializer
    queryset=UserOffers.objects.all()


class GetPastUserAppointments(generics.ListAPIView):
    permission_classes = [IsVerified]
    serializer_class = PastAppointmentDetailSerializer

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        return Appointments.objects.filter(patient=user, date__lt=today).order_by('-date')

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


