from django.urls import path
from .views import (
    AttendanceListView,
    AttendanceCreateView,
    AttendanceRetrieveView,
    AttendanceUpdateView,
    AttendanceDestroyView,
    AttendanceByDateView,
    AttendanceStatsView,
    AttendanceExportView2,
    AttendanceEmployeesView,
    AttendanceDepartmentsView,
    AttendanceDateRangeSummaryView
)

urlpatterns = [
    path('list/', AttendanceListView.as_view(), name='attendance-list'),
    path('create/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('export/', AttendanceExportView2.as_view(), name='attendance-export'),
    path('by-date/', AttendanceByDateView.as_view(), name='attendance-by-date'),
    path('employees/', AttendanceEmployeesView.as_view(), name='attendance-employees'),
    path('departments/', AttendanceDepartmentsView.as_view(), name='attendance-departments'),
    path('summary/', AttendanceDateRangeSummaryView.as_view(), name='attendance-date-range-summary'),
    path('details/<str:attendance_id>/', AttendanceRetrieveView.as_view(), name='attendance-detail'),
    path('update/<str:attendance_id>/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('delete/<str:attendance_id>/', AttendanceDestroyView.as_view(), name='attendance-delete'),
]
