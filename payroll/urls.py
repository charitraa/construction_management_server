from django.urls import path
from .views import (
    PayrollByMonthView,
    PayrollMarkAsPaidView,
    PayrollSummaryView,
    PayrollExportView
)

urlpatterns = [
    path('by-date/', PayrollByMonthView.as_view(), name='payroll-by-date'),
    path('summary/', PayrollSummaryView.as_view(), name='payroll-summary'),
    path('export/', PayrollExportView.as_view(), name='payroll-export'),
    path('pay/',     PayrollMarkAsPaidView.as_view(), name='payroll-pay'),
]
