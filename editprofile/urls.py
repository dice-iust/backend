from django.urls import path
from .views import UserProfileUpdateAPIView,putmethod

urlpatterns = [
    path("update/", UserProfileUpdateAPIView.as_view(), name="user-profile-update"),
    path("update_2/", putmethod.as_view()),
]
