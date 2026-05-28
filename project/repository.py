from django.db import models
from .models import Project


class ProjectRepository:
    
    @staticmethod
    def get_all():
        return Project.objects.all()
    
    @staticmethod
    def get_by_id(project_id):
        return Project.objects.filter(id=project_id).first()
    
    @staticmethod
    def get_by_location(location):
        return Project.objects.filter(location__icontains=location)
    
    @staticmethod
    def create_project(project_data):
        return Project.objects.create(**project_data)
    
    @staticmethod
    def update_project(project, update_data):
        for key, value in update_data.items():
            setattr(project, key, value)
        project.save()
        return project
    
    @staticmethod
    def delete_project(project):
        project.delete()
    
    @staticmethod
    def count_all():
        return Project.objects.count()

    @staticmethod
    def get_by_status(status):
        return Project.objects.filter(status=status)

    @staticmethod
    def get_active_projects_count():
        return Project.objects.filter(status='ongoing').count()

    @staticmethod
    def count_by_status():
        from django.db.models import Count
        result = Project.objects.values('status').annotate(count=Count('id'))
        return {item['status']: item['count'] for item in result}

    @staticmethod
    def get_receivables():
        """Annotate each project with the total revenue actually received from the client.

        Only revenue marked 'Received' counts as paid; Pending/Overdue is still owed.
        """
        from django.db.models.functions import Coalesce

        received = Coalesce(
            models.Sum(
                'revenues__amount',
                filter=models.Q(revenues__status='Received'),
            ),
            models.Value(0, output_field=models.DecimalField(max_digits=15, decimal_places=2)),
        )
        return Project.objects.annotate(received=received)