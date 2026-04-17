from django.db import models
from .models import Employee


class EmployeeRepository:
    
    @staticmethod
    def get_all():
        return Employee.objects.all()
    
    @staticmethod
    def get_by_id(employee_id):
        return Employee.objects.filter(id=employee_id).first()
    
    @staticmethod
    def get_by_role(role):
        return Employee.objects.filter(role=role)
    
    @staticmethod
    def create_employee(employee_data):
        return Employee.objects.create(**employee_data)
    
    @staticmethod
    def update_employee(employee, update_data):
        for key, value in update_data.items():
            setattr(employee, key, value)
        employee.save()
        return employee
    
    @staticmethod
    def delete_employee(employee):
        employee.delete()
    
    @staticmethod
    def count_all():
        return Employee.objects.count()
    
    @staticmethod
    def count_by_role(role):
        return Employee.objects.filter(role=role).count()