from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import LoginRequiredPermission
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
        if location:
            projects = ProjectService.get_projects_by_location(location)
        else:
            projects = ProjectService.get_all_projects()
        return Response({
            "data": ProjectService.serialize_projects(projects),
            "message": "Project list retrieved successfully"
        }, status=status.HTTP_200_OK)


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


class ProjectExportView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        location = request.query_params.get('location')
        if location:
            projects = ProjectService.get_projects_by_location(location)
        else:
            projects = ProjectService.get_all_projects()
        
        if not projects.exists():
            return Response({
                "error": "No projects to export"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Project ID', 'Project Name', 'Client', 'Location', 'Value'])
        
        for proj in projects:
            writer.writerow([str(proj.id), proj.name, proj.client_name, proj.location, proj.contract_value])
        
        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Projects exported successfully"
        }, status=status.HTTP_200_OK)