from django.urls import path
from .views import (
    DashboardOverviewView,
    DashboardStatsView,
    MonthlyTrendsView,
    ExpenseDistributionView,
    QuickStatsView,
    DashboardExportView
)

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('trends/', MonthlyTrendsView.as_view(), name='dashboard-trends'),
    path('expenses/', ExpenseDistributionView.as_view(), name='dashboard-expenses'),
    path('quick-stats/', QuickStatsView.as_view(), name='dashboard-quick-stats'),
    path('export/', DashboardExportView.as_view(), name='dashboard-export'),
]
