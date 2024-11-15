from django.db import models
from signup.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# from editprofile.models import UserProfile

class Travel(models.Model):
    type1='Budget-friendly'
    type2='Fancy'
    type_choices=[
        ('Budget-friendly',type1),
        ('Fancy',type2)
    ]
    trans1='Train'
    trans2='Bus'
    trans3='Plane'
    trans4='Car'
    trans_choices=[
        ("Train",trans1),
        ("Bus",trans2),
        ("Plane",trans3),
        ("Car",trans4)
    ]
    admin=models.OneToOneField(User,on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now_add=False)
    photo = models.ImageField(upload_to="profiles",blank=True,)
    destination = models.CharField(max_length=200)
    mode=models.CharField(max_length=200,choices=type_choices)
    start_place=models.CharField(max_length=200)
    transportation=models.CharField(max_length=200,choices=trans_choices)
    end_date=models.DateTimeField(auto_now_add=False)   
    travellers=models.IntegerField(blank=False,default=5)
    def __str__(self):
        return self.destination
