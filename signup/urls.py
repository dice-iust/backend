from django.urls import path
from signup.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	UserLogoutViewAPI,UserRegistrationAndVerificationAPIView,EmailVerificationView)
from django.conf.urls.static import static
from django.conf import settings
from .views import ForgotPasswordView, PasswordResetConfirmView
urlpatterns = [
    
	path('user/register/', UserRegistrationAPIView.as_view()),
	path('user/login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	path('user/logout/', UserLogoutViewAPI.as_view()),
	path('user/signup/',UserRegistrationAndVerificationAPIView.as_view()),path("send/",EmailVerificationView.as_view()),
	path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

]

