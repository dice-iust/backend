from django.urls import path
from .views import CreateExpenseAPIView, DebtsAPIView, SettleDebtAPIView

urlpatterns = [
    path("travels/<int:travel_name>/expenses/", CreateExpenseAPIView.as_view(), name="create-expense"),
    path("travels/<int:travel_name>/debts/", DebtsAPIView.as_view(), name="view-debts"),
    path("settle-debt/", SettleDebtAPIView.as_view(), name="settle-debt"),
]
