from django.urls import path
from .views import (
    RevenueListView,
    RevenueCreateView,
    RevenueRetrieveView,
    RevenueUpdateView,
    RevenueDestroyView,
    RevenueStatsView,
    RevenueExportView
)

urlpatterns = [
    path('list/', RevenueListView.as_view(), name='revenue-list'),
    path('create/', RevenueCreateView.as_view(), name='revenue-create'),
    path('stats/', RevenueStatsView.as_view(), name='revenue-stats'),
    path('export/', RevenueExportView.as_view(), name='revenue-export'),
    path('details/<str:revenue_id>/', RevenueRetrieveView.as_view(), name='revenue-detail'),
    path('update/<str:revenue_id>/', RevenueUpdateView.as_view(), name='revenue-update'),
    path('delete/<str:revenue_id>/', RevenueDestroyView.as_view(), name='revenue-delete'),
]