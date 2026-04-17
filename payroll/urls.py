from django.urls import path
from .views import (
    PayrollByMonthView,
    PayrollSummaryView,
    PayrollExportView
)

urlpatterns = [
    path('by-month/', PayrollByMonthView.as_view(), name='payroll-by-month'),
    path('summary/', PayrollSummaryView.as_view(), name='payroll-summary'),
    path('export/', PayrollExportView.as_view(), name='payroll-export'),
]
