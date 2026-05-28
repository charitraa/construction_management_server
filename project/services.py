from .repository import ProjectRepository
from .serializers import ProjectSerializer, ProjectReceivableSerializer


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
            "ongoing": ProjectRepository.get_active_projects_count(),
            "by_status": ProjectRepository.count_by_status()
        }

    @staticmethod
    def get_receivables():
        return ProjectRepository.get_receivables()

    @staticmethod
    def serialize_receivables(projects):
        return ProjectReceivableSerializer(projects, many=True).data

    @staticmethod
    def get_receivables_summary(rows):
        """Roll up serialized receivable rows into headline totals."""
        total_budget = sum(row['budget'] for row in rows)
        total_received = sum(row['received'] for row in rows)
        total_remaining = sum(row['remaining'] for row in rows)
        return {
            "total_budget": round(total_budget, 2),
            "total_received": round(total_received, 2),
            "total_remaining": round(total_remaining, 2),
            "projects_count": len(rows),
            "clients_with_dues": len({
                row['client_name'] for row in rows if row['remaining'] > 0
            }),
        }