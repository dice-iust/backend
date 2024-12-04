from django.urls import path
from .views import profileView
urlpatterns= [

    path("profile/", profileView.as_view()),
]
