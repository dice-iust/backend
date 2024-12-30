from django.contrib import admin
from . models import Expense,Settlement,PastPayment,ExpensePayment
# Register your models here.
admin.site.register(Expense)
admin.site.register(Settlement)
admin.site.register(PastPayment)
admin.site.register(ExpensePayment)