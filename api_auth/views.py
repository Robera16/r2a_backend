from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import (
    UserSerializer, StateSerializers, DistrictSerializers, 
    ConstituencySerializers, SingInSerializer, ChangePasswordSerializer, CountrySerializers, PhoneOtpSerializer
    )
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .models import ( 
    PhoneOtp, User, State,  District, Constituency, Country
    )
import random
import pyotp
import os
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import IntegrityError
from django.db.models import Q
from django.core.mail import send_mail

#Whener this is changed for login change OptLoginView class as well because it is OTP Auth 
class SignInView(TokenObtainPairView):
    serializer_class = SingInSerializer

sender_email = os.environ['EMAIL_HOST_USER']
#Generate a OTP
#TODO: move api url to env
def get_otp(phone_number, email, country):
    
    totp = pyotp.TOTP('base32secret3232')
    key = totp.now()
    text = "Hello , \n Your OTP from Infliq is {otp}".format(otp=key)
    if country.name.lower() == 'india':    
        url = 'http://login.adwingssolutions.com/api/v1/sendSMS.php?APIKey={api_key}&senderid={sender_id}&flashsms=0&number={phone_number}&text={text}'.format(api_key=os.environ['SMS_API_KEY'], sender_id=os.environ['SMS_SENDER_ID'], phone_number=phone_number,text=text)
        try:
            response = requests.get(url)
            if response.status_code == 200: 
                return key
            else:
                return False
        except:
            return False
    else:
        try:
            send_mail(
                'Right2Ask OTP request',
                text,
                sender_email,
                [email],
                fail_silently=False,
            )
            return key
        except Exception:
            return False


# Generates otp for login
#TODO: *IMP* Validate phonenumber is valid (length) same for registration 
class GenerateLoginOtpView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            try:
                user = User.objects.get(phone_number__iexact=phone_number)
                if user:
                    if user.attempts < 5:
                        # key = get_otp(phone_number, user.email, user.country)
                        otp='123456'
                        if key:
                            user.otp = key
                            user.attempts  += 1
                            user.save()
                            return Response({
                                'status': 'ok',
                                'message': 'otp sent sucessfuly',
                                'CODE': 'OTP_SUCCESS'
                            })
                        else:
                            return Response({
                                'status': 'bad',
                                'message': 'Problem sending otp',
                                'CODE': 'OTP_PROBLEM'
                            })
                    else:
                        return Response({
                            'status': 'bad',
                            'message': 'Limit Exceeded Please try again after 20 minutes',
                            'CODE': 'USER_NOT_FOUND'
                            })
                else:
                    return Response({
                        'status': 'bad',
                        'message': 'Complete registation to continue login',
                        'CODE': 'USER_NOT_FOUND'
                    })
            except User.DoesNotExist:
                return Response({
                    "status": "bad",
                    "message": "User does not exists",
                    "CODE": "USER_NOT_EXISTS"
                })
        else:
            return Response({
                'status': 'bad',
                'message': 'phone_number is required field',
                'CODE': 'PARAM_REQUIRED_PHONE'
            })

#Login with the otp generated above and creates a token
#TODO implement otps limit per day/hour and reject user from sending more otps

#Wheneber this class is modified for some auth suff also refect the same in SignInView classes serializer
class OptLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if phone_number and otp:
            try:
                user = User.objects.get(phone_number = phone_number, otp = otp)
            except User.DoesNotExist:
                return Response({'message': 'Invalid OTP ', 'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.admin:
                return Response({'message': 'Admin Cannot login on Mobile App ', 'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                refresh = RefreshToken.for_user(user)
                user.otp = ''
                user.attempts = 0
                user.save()
                return Response({
                            'status': 'ok',
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'first_name': user.first_name,
                            'username': user.username,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'id': user.id,
                            'avatar_url': user.profile.avatar.url,
                            'can_create': user.can_create,
                            "role": user.role,
                            "is_admin": user.admin,
                            "foreign_user": user.foreign_user,
                            'CODE': 'AUTH_SUCCESS'
                            })
        else:
            return Response({   
                'status': 'bad',
                'message': 'otp and phone number a required',
                'CODE': 'PARAM_REQUIRED_PHONE_AND_OTP'
            })

@api_view(['POST'])
def email_login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    print(email)
    print(password)
    if email and password:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'No Account with given email ', 'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
            if user.admin:
                return Response({'detail': 'Admin Cannot login on Mobile App ', 'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                refresh = RefreshToken.for_user(user)
                print('refersh', str(refresh))
                print('access' ,str(refresh.access_token))
                user.otp = ''
                user.attempts = 0
                user.save()
                return Response({
                            'status': 'ok',
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'first_name': user.first_name,
                            'username': user.username,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'id': user.id,
                            'avatar_url': user.profile.avatar.url,
                            'can_create': user.can_create,
                            "role": user.role,
                            "is_admin": user.admin,
                            "foreign_user": user.foreign_user,
                            'CODE': 'AUTH_SUCCESS'
                            })
        else:
            return Response({'detail': 'Password Does Not Match ', 'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({   
                'status': 'bad',
                'message': 'email and password a required',
                'CODE': 'PARAM_REQUIRED_PHONE_AND_OTP'
            })


#Register user after phone_number is validated
#TODO:  use email, phone number and country from otp verified only 
#Now we only check by phone number and verified state but need to change it to get country from there it self
class RegisterView(APIView):
    def post(self, request):
        user_data = request.data
        phone_number = request.data.get('phone_number')
      
        try:
            serializer = UserSerializer(data= user_data)
            if serializer.is_valid(raise_exception=True):
                    serializer.save()
            return Response({"status": 'OK', "data": serializer.data})
        except IntegrityError:
            return Response({"status": 'bad', "data": "User Exists with given Email Address"}, status=status.HTTP_400_BAD_REQUEST)
               
         
    

    # def post(self, request):
    #     user_data = request.data
    #     phone_number = request.data.get('phone_number')
    #     old  = PhoneOtp.objects.filter(phone_number__iexact = phone_number)
    #     if old:
    #         validated = old.first().validated
    #         if validated:
    #             if validated:
    #                 try:
    #                     serializer = UserSerializer(data= user_data)
    #                     if serializer.is_valid(raise_exception=True):
    #                         serializer.save()
    #                     return Response({"status": 'OK', "data": serializer.data})
    #                 except IntegrityError:
    #                     return Response({"status": 'bad', "data": "User Exists with given Email Address"}, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 return Response({
    #                     "status": "bad",
    #                     "message": "Validate phone number to continue registartion",
    #                     "CODE": 'USER_NOT_VALIDATED'
    #                 })
    #         else:
    #             return Response({
    #                 'status': 'bad',
    #                 'message': 'validate your mobile number to register'
    #             })
    #     else:
    #         return Response({
    #                 'status': 'bad',
    #                 'message': 'validate your mobile number to register'
    #             })



"""
    to check if username is already taken
"""
@api_view(['POST'])
def check_user_name(request):
    username = request.data.get('username')
    try:
        User.objects.get(username = username)
        return Response({
            "message": username  + " already taken."
        }, status=status.HTTP_409_CONFLICT)
    except User.DoesNotExist:
        return Response({
            "message": username + " is available."
        })
    except Exception as e:
        print("Error: check_user_name -> ", e)
        return Response({
            "message": "something went wrong please try again"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#Generates OTP for registration
#TODO implement otps limit (done) enhance per day/hour and reject user from sending more otps

class GenerateOtpView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        country_id = request.data.get('country')
        if phone_number  and country_id:
            user = User.objects.filter(phone_number__iexact = phone_number)
            try :
                country = Country.objects.get(pk=country_id)
            except Country.DoesNotExist:
                return Response({
                    "status": "bad",
                    "msg": "Country is not registered "
                })
            if user:
                return Response({
                    "status": "bad",
                    "msg": "phone number is already taken"
                })
            else:
                #TODO Check and re write the below part for sms attemps (limit) 
                #Should not send if the limit has exceeded and write a logic to reset the count 0 on basis on their business logic basically reset to zero after every 24 hours or 1 hr
                #letting it be for now .... Development purposes

                otpModel = PhoneOtp.objects.filter(Q(phone_number__iexact = phone_number)).distinct()
                if otpModel.exists():
                    try:
                        otpModel.delete()
                        phone = otpModel.first()
                    except Exception:
                        return Response({
                            "status": "bad",
                            "msg": "Some Thing Went Wrong Please try again..."
                        })
                # otp =  get_otp(phone_number, '', country)
                otp='123456'
                if otp:
                    phone = PhoneOtp(
                        phone_number  = phone_number,
                        otp = otp,
                        country = country      
                        )
                    phone.save()
                    return Response({
                            'status': 'ok',
                            'message': 'otp generated'
                        })
                else:
                    return Response({
                        "status": "bad",
                        "message": "Problem sending OTP"
                    })
        else:
            return Response({"status": "bad", "msg": "phone Number, country are mandatory"})

#Validates phone number before registration
class ValidateOtpView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if otp and phone_number:
            old = PhoneOtp.objects.filter(Q(phone_number__iexact = phone_number) )
            if old.exists():
                old = old.first()
                if str(old.otp) == str(otp):
                    old.validated = True
                    old.otp = ''
                    old.save()
                    serialize = PhoneOtpSerializer(instance=old)                    
                    return Response({
                        'status': 'ok',
                        'message': 'Validated sucessfully',
                        'data': serialize.data
                    })
                else:
                    return Response({
                        'status': 'bad',
                        'message': 'Otp did not match'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'status': 'bad',
                    'message': 'Enter a valid number '
                })
        else:
            return Response({
                'status': 'bad',
                'message': 'opt and phone number are mandatory'
            })

class StatesView(ListAPIView):

    def list(self, request):
        queryset = State.objects.all()
        serializer = StateSerializers(queryset, many=True)
        response_list = serializer.data
        return Response({
            "status": "ok",
            "message": "states list",
            "data": response_list
        })

class CountriesView(ListAPIView):
    
    def list(self, request):
        queryset = Country.objects.all()
        serializer = CountrySerializers(queryset, many = True)
        response_list = serializer.data
        return Response({
                "status": "ok",
                "message": "countries list",
                "data": response_list
                })

class StateDistrictView(ListAPIView):

    def list(self, request, pk):
        queryset = District.objects.filter(state_id=pk)
        serializer = DistrictSerializers(queryset, many=True)
        response_list = serializer.data
        return Response({
            "status": "ok",
            "message": "Districts list for state",
            "data": response_list
        })

class DistrictConstituencyView(ListAPIView):

    def list(self, request, pk):
        queryset = Constituency.objects.filter(district_id=pk)
        serializer = ConstituencySerializers(queryset, many=True)
        response_list = serializer.data
        return Response({
            "status": "ok",
            "message": "Constituency List for District",
            "data": response_list
        })

@api_view(['POST'])
def forgot_password_otp(request):
    print("here")
    phone_number = request.data.get('phone_number')
    user = User.objects.filter(phone_number__iexact = phone_number)
    if user.exists():
        user = user.first()
        if user.attempts < 5:
            # key = get_otp(phone_number, user.email, user.country)
            otp='123456'

            if key:
                user.otp = key
                user.attempts += 1
                user.save()
                return Response({
                    "status": "ok",
                    "message": "OTP send sucessfully",
                    "CODE": "OTP_SENT"
                })
            else:
                return Response({
                    "status": "bad",
                    "message": "Problem sending OTP please try again "
                })
        else:
            return Response({
                "status": "bad",
                "message": "Limit Exceeded Please try again after 20 minutes"
            })
    else:
        return Response({
            "status": "bad",
            "message": "User Does not exists with the Phone Number",
            "CODE": "USER_NOT_EXISTS"
        })

@api_view(['POST'])
def reset_password_view(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    password = request.data.get('password')

    if phone_number and otp and password:
        user = User.objects.filter(phone_number__iexact = phone_number)
        if user.exists():
            user = user.first()
            if user.otp == otp:
                user.set_password(password)
                user.otp = ''
                user.attempts = 0
                user.save()
                return Response({
                    "status": "ok",
                    "message": "Password Change Sucess"
                })
            else:
                return Response({
                    "status": "bad",
                    "message": "OTP does not match"
                })

        else:
            return Response({
                "status": "bad",
                "message": "User doesnot exists with the phone number",
                "CODE": "USER_NOT_EXISTS"
            })
    else:
        return Response({
            "status": "bad",
            "message": "phone number , otp, password are required to reset"
        })


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
