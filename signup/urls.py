from django.urls import path
from signup.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	UserLogoutViewAPI,UserRegistrationAndVerificationAPIView,EmailVerificationView)
from django.conf.urls.static import static
from django.conf import settings
from .views import PasswordResetRequestAPIView, PasswordResetVerifyAPIView
urlpatterns = [
    

	path('user/login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	path('user/logout/', UserLogoutViewAPI.as_view()),
	path('user/register/',UserRegistrationAndVerificationAPIView.as_view()),path("send/",EmailVerificationView.as_view()),
	path('password-reset-request/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset-verify/', PasswordResetVerifyAPIView.as_view(), name='password-reset-verify'),

]

