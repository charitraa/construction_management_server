from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
from core.pagination import StandardPagination
from django.db import models
from .serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer
)
from .services import ProjectService
from .exceptions import ProjectNotFoundException
import csv
import io


class ProjectListView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        location = request.query_params.get('location')
        status_param = request.query_params.get('status')

        if location and status_param:
            projects = ProjectService.get_projects_by_location(location).filter(status=status_param)
        elif location:
            projects = ProjectService.get_projects_by_location(location)
        elif status_param:
            projects = ProjectService.get_projects_by_status(status_param)
        else:
            projects = ProjectService.get_all_projects()

        paginator = StandardPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)
        return paginator.get_paginated_response(
            ProjectService.serialize_projects(paginated_projects),
            "Project list retrieved successfully"
        )


class ProjectCreateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response({
                "data": ProjectService.serialize_project(project),
                "message": "Project created successfully"
            }, status=status.HTTP_201_CREATED)


class ProjectRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, project_id, *args, **kwargs):
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundException("Project not found.")
        return Response({
            "data": ProjectService.serialize_project(project),
            "message": "Project details retrieved successfully"
        }, status=status.HTTP_200_OK)


class ProjectUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]

    def put(self, request, project_id, *args, **kwargs):
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundException("Project not found.")
        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response({
                "data": ProjectService.serialize_project(project),
                "message": "Project updated successfully"
            }, status=status.HTTP_200_OK)


class ProjectDestroyView(APIView):
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, project_id, *args, **kwargs):
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundException("Project not found.")
        ProjectService.delete_project(project)
        return Response({
            "message": "Project deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class ProjectStatsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        stats = ProjectService.get_project_stats()
        return Response({
            "data": stats,
            "message": "Project statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class ProjectReceivablesView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        """Per-project outstanding amounts owed by clients (budget - received)."""
        search = request.query_params.get('search')
        status_param = request.query_params.get('status')
        outstanding_only = request.query_params.get('outstanding_only')

        projects = ProjectService.get_receivables()

        if search:
            projects = projects.filter(
                models.Q(name__icontains=search) |
                models.Q(client_name__icontains=search) |
                models.Q(location__icontains=search)
            )

        if status_param:
            projects = projects.filter(status=status_param)

        rows = ProjectService.serialize_receivables(projects)

        if outstanding_only in ('1', 'true', 'True'):
            rows = [row for row in rows if row['remaining'] > 0]

        summary = ProjectService.get_receivables_summary(rows)

        return Response({
            "data": rows,
            "summary": summary,
            "message": "Project receivables retrieved successfully"
        }, status=status.HTTP_200_OK)


class ProjectExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        location = request.query_params.get('location')
        status_param = request.query_params.get('status')

        if location and status_param:
            projects = ProjectService.get_projects_by_location(location).filter(status=status_param)
        elif location:
            projects = ProjectService.get_projects_by_location(location)
        elif status_param:
            projects = ProjectService.get_projects_by_status(status_param)
        else:
            projects = ProjectService.get_all_projects()

        if not projects.exists():
            return Response({
                "error": "No projects to export"
            }, status=status.HTTP_400_BAD_REQUEST)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Project ID', 'Project Name', 'Description', 'Client', 'Location', 'Start Date', 'Status', 'Budget'])

        for proj in projects:
            writer.writerow([
                str(proj.id),
                proj.name,
                proj.description or '',
                proj.client_name,
                proj.location,
                str(proj.start_date) if proj.start_date else '',
                proj.status,
                str(proj.budget)
            ])

        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Projects exported successfully"
        }, status=status.HTTP_200_OK)