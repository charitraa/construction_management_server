from django.urls import path
from .views import (
    AdvanceListView,
    AdvanceCreateView,
    AdvanceRetrieveView,
    AdvanceDestroyView,
    AdvanceStatsView
)

urlpatterns = [
    path('list/', AdvanceListView.as_view(), name='advance-list'),
    path('create/', AdvanceCreateView.as_view(), name='advance-create'),
    path('stats/', AdvanceStatsView.as_view(), name='advance-stats'),
    path('details/<str:advance_id>/', AdvanceRetrieveView.as_view(), name='advance-detail'),
    path('delete/<str:advance_id>/', AdvanceDestroyView.as_view(), name='advance-delete'),
]