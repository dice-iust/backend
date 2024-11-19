
from django.urls import path
from .views import UserProfileUpdateAPIView

urlpatterns = [
    path('update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
]

