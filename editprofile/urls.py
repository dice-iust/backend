from django.urls import path
from .views import UserProfileView  # Assuming you have a UserProfileView class in views.py

urlpatterns = [
    
    path('', UserProfileView.as_view(), name='editprofile'),
]
