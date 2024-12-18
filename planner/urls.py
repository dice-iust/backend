from django.urls import path
from .views import CreateExpenseAPIView, DebtsAPIView, AllPayView, MarkAsPaidAPIView

urlpatterns = [
    path("travels/expenses/", CreateExpenseAPIView.as_view(), name="create-expense"),
    path("travels/debts/", DebtsAPIView.as_view(), name="view-debts"),
    path('allpay/', AllPayView.as_view()),
    path("travels/mark-as-paid/", MarkAsPaidAPIView.as_view(), name="mark-as-paid"),
]


