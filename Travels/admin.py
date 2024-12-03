from django.contrib import admin
from .models import *
admin.site.register(TravellersGroup)
admin.site.register(Travel)
admin.site.register(UserRate)
admin.site.register(TravelUserRateMoney)
admin.site.register(TravelUserRateSleep)