from .repository import EmployeeRepository
from .serializers import EmployeeSerializer


class EmployeeService:
    
    @staticmethod
    def get_all_employees():
        return EmployeeRepository.get_all()
    
    @staticmethod
    def get_employee_by_id(employee_id):
        return EmployeeRepository.get_by_id(employee_id)
    
    @staticmethod
    def get_employees_by_role(role):
        return EmployeeRepository.get_by_role(role)
    
    @staticmethod
    def create_employee(employee_data):
        return EmployeeRepository.create_employee(employee_data)
    
    @staticmethod
    def update_employee(employee, update_data):
        return EmployeeRepository.update_employee(employee, update_data)
    
    @staticmethod
    def delete_employee(employee):
        EmployeeRepository.delete_employee(employee)
    
    @staticmethod
    def serialize_employee(employee):
        return EmployeeSerializer(employee).data
    
    @staticmethod
    def serialize_employees(employees):
        return EmployeeSerializer(employees, many=True).data
    
    @staticmethod
    def get_employee_stats():
        return {
            "total": EmployeeRepository.count_all(),
            "Labor": EmployeeRepository.count_by_role('Labor'),
            "Mason": EmployeeRepository.count_by_role('Mason')
        }