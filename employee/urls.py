from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeRetrieveView,
    EmployeeUpdateView,
    EmployeeDestroyView,
    EmployeeStatsView,
    EmployeeExportView
)

urlpatterns = [
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('stats/', EmployeeStatsView.as_view(), name='employee-stats'),
    path('export/', EmployeeExportView.as_view(), name='employee-export'),
    path('details/<str:employee_id>/', EmployeeRetrieveView.as_view(), name='employee-detail'),
    path('update/<str:employee_id>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('delete/<str:employee_id>/', EmployeeDestroyView.as_view(), name='employee-delete'),
]