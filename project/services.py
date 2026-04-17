from .repository import ProjectRepository
from .serializers import ProjectSerializer


class ProjectService:

    @staticmethod
    def get_all_projects():
        return ProjectRepository.get_all()

    @staticmethod
    def get_project_by_id(project_id):
        return ProjectRepository.get_by_id(project_id)

    @staticmethod
    def get_projects_by_location(location):
        return ProjectRepository.get_by_location(location)

    @staticmethod
    def get_projects_by_status(status):
        return ProjectRepository.get_by_status(status)

    @staticmethod
    def create_project(project_data):
        return ProjectRepository.create_project(project_data)

    @staticmethod
    def update_project(project, update_data):
        return ProjectRepository.update_project(project, update_data)

    @staticmethod
    def delete_project(project):
        ProjectRepository.delete_project(project)

    @staticmethod
    def serialize_project(project):
        return ProjectSerializer(project).data

    @staticmethod
    def serialize_projects(projects):
        return ProjectSerializer(projects, many=True).data

    @staticmethod
    def get_project_stats():
        return {
            "total": ProjectRepository.count_all(),
            "total_value": ProjectRepository.total_contract_value(),
            "ongoing": ProjectRepository.get_active_projects_count(),
            "by_status": ProjectRepository.count_by_status()
        }