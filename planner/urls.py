# urls.py در اپ planner
from django.urls import path
from .views import CreateExpenseAPIView, DebtsAPIView, SettleDebtAPIView

urlpatterns = [
    path("travels/<int:travel_id>/expenses/", CreateExpenseAPIView.as_view(), name="create-expense"),
    path("travels/<int:travel_id>/debts/", DebtsAPIView.as_view(), name="view-debts"),
    path("settle-debt/", SettleDebtAPIView.as_view(), name="settle-debt"),
]
