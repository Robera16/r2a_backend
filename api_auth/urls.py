from django.urls import path
from .views import ( 
    RegisterView, GenerateOtpView, ValidateOtpView, GenerateLoginOtpView, 
    OptLoginView, StatesView, StateDistrictView, DistrictConstituencyView,
    forgot_password_otp, reset_password_view, SignInView,
    ChangePasswordView, CountriesView, email_login_view, check_user_name
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('sign_in/', SignInView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_otp/', GenerateOtpView.as_view()),
    path('validate_phone/', ValidateOtpView.as_view()),
    # path('generate_login_otp/', GenerateLoginOtpView.as_view()), deprecated
    # path('otp_login/', OptLoginView.as_view()), deprecated
    path('countries/', CountriesView.as_view()),
    path('states/', StatesView.as_view()),
    path('districts/<int:pk>/', StateDistrictView.as_view()),
    path('constituencies/<int:pk>/', DistrictConstituencyView.as_view()),
    path('forgot_password_otp/', forgot_password_otp),
    path('reset_password/', reset_password_view),
    path('change_password/', ChangePasswordView.as_view()),
    path('email_login/', email_login_view),
    path('check_username/', check_user_name)
]