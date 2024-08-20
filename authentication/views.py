from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import CustomUser
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import random
import requests
from rest_framework.permissions import BasePermission,AllowAny
from django.core.exceptions import ObjectDoesNotExist

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

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class UserRegistration(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            name = request.data.get('name')
            number = request.data.get('phoneNumber')
            if not name or not number:
                return Response({"message": "Name and number are required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user=CustomUser.objects.get(phone=number)
                if user is not None:
                    return Response({"message":"User exists!"},status=200)

            except:
                user = CustomUser.objects.create(name=name, phone=number)
                user.otp = random.randint(1000, 9999)
                user.save()
                token = get_tokens(user)
                check = send_otp(number, user.otp)
                if check:
                    return Response({"message": "OTP generated successfully", "token": token,"status":201}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "OTP not generated", "token": token,"status":400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "OTP not generated", "error": str(e),"status":400}, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            number = request.data.get('number')
            if not number:
                return Response({"message": "Number is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.get(phone=number)
            user.otp = random.randint(1000, 9999)
            user.save()
            token = get_tokens(user)
            check = send_otp(number, user.otp)
            if check:
                return Response({"message": "OTP generated successfully", "token": token}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "OTP not generated", "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "No user found with these credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "OTP not generated", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(generics.CreateAPIView):
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
                return Response({"message": "Authenticated Successfully","user":user}, status=200)
            else:
                return Response({"message": "Authentication failed"}, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=500)

              
