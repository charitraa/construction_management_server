from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    ProjectRetrieveView,
    ProjectUpdateView,
    ProjectDestroyView,
    ProjectStatsView,
    ProjectExportView
)

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('stats/', ProjectStatsView.as_view(), name='project-stats'),
    path('export/', ProjectExportView.as_view(), name='project-export'),
    path('details/<str:project_id>/', ProjectRetrieveView.as_view(), name='project-detail'),
    path('update/<str:project_id>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<str:project_id>/', ProjectDestroyView.as_view(), name='project-delete'),
]