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
    def total_contract_value():
        from django.db.models import Sum
        return Project.objects.aggregate(total=Sum('contract_value'))['total'] or 0