# urls.py در اپ planner
from django.urls import path
from .views import CreateExpenseAPIView, DebtsAPIView, SettleDebtAPIView,AllPayView

urlpatterns = [
    path("travels/expenses/", CreateExpenseAPIView.as_view(), name="create-expense"),
    path("travels/debts/", DebtsAPIView.as_view(), name="view-debts"),
    path("settle-debt/", SettleDebtAPIView.as_view(), name="settle-debt"),
    path('allpay/', AllPayView.as_view()),
]


