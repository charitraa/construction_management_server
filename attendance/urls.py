from django.urls import path
from .views import (
    AttendanceListView,
    AttendanceCreateView,
    AttendanceRetrieveView,
    AttendanceUpdateView,
    AttendanceDestroyView,
    AttendanceByDateView,
    AttendanceStatsView,
    AttendanceExportView
)

urlpatterns = [
    path('list/', AttendanceListView.as_view(), name='attendance-list'),
    path('create/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('export/', AttendanceExportView.as_view(), name='attendance-export'),
    path('by-date/', AttendanceByDateView.as_view(), name='attendance-by-date'),
    path('details/<str:attendance_id>/', AttendanceRetrieveView.as_view(), name='attendance-detail'),
    path('update/<str:attendance_id>/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('delete/<str:attendance_id>/', AttendanceDestroyView.as_view(), name='attendance-delete'),
]
