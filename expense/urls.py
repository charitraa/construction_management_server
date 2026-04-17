from django.urls import path
from .views import (
    ExpenseListView,
    ExpenseCreateView,
    ExpenseRetrieveView,
    ExpenseUpdateView,
    ExpenseDestroyView,
    ExpenseStatsView,
    ExpenseExportView
)

urlpatterns = [
    path('list/', ExpenseListView.as_view(), name='expense-list'),
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('stats/', ExpenseStatsView.as_view(), name='expense-stats'),
    path('export/', ExpenseExportView.as_view(), name='expense-export'),
    path('details/<str:expense_id>/', ExpenseRetrieveView.as_view(), name='expense-detail'),
    path('update/<str:expense_id>/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('delete/<str:expense_id>/', ExpenseDestroyView.as_view(), name='expense-delete'),
]