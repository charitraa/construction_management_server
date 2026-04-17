from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.permission import HasPageAccess
from core.permission import LoginRequiredPermission
from .serializers import (
    EmployeeSerializer,
    EmployeeCreateSerializer,
    EmployeeUpdateSerializer
)
from .services import EmployeeService
from .exceptions import EmployeeNotFoundException
import csv
import io


class EmployeeListView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        role = request.query_params.get('role')
        if role:
            employees = EmployeeService.get_employees_by_role(role)
        else:
            employees = EmployeeService.get_all_employees()
        return Response({
            "data": EmployeeService.serialize_employees(employees),
            "message": "Employee list retrieved successfully"
        }, status=status.HTTP_200_OK)


class EmployeeCreateView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def post(self, request, *args, **kwargs):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee = serializer.save()
            return Response({
                "data": EmployeeService.serialize_employee(employee),
                "message": "Employee created successfully"
            }, status=status.HTTP_201_CREATED)


class EmployeeRetrieveView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, employee_id, *args, **kwargs):
        employee = EmployeeService.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException("Employee not found.")
        return Response({
            "data": EmployeeService.serialize_employee(employee),
            "message": "Employee details retrieved successfully"
        }, status=status.HTTP_200_OK)


class EmployeeUpdateView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def put(self, request, employee_id, *args, **kwargs):
        employee = EmployeeService.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException("Employee not found.")
        serializer = EmployeeUpdateSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            employee = serializer.save()
            return Response({
                "data": EmployeeService.serialize_employee(employee),
                "message": "Employee updated successfully"
            }, status=status.HTTP_200_OK)


class EmployeeDestroyView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def delete(self, request, employee_id, *args, **kwargs):
        employee = EmployeeService.get_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException("Employee not found.")
        EmployeeService.delete_employee(employee)
        return Response({
            "message": "Employee deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class EmployeeStatsView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        stats = EmployeeService.get_employee_stats()
        return Response({
            "data": stats,
            "message": "Employee statistics retrieved successfully"
        }, status=status.HTTP_200_OK)


class EmployeeExportView(APIView):
    permission_classes = [LoginRequiredPermission, HasPageAccess]

    def get(self, request, *args, **kwargs):
        role = request.query_params.get('role')
        if role:
            employees = EmployeeService.get_employees_by_role(role)
        else:
            employees = EmployeeService.get_all_employees()
        
        if not employees.exists():
            return Response({
                "error": "No employees to export"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Role', 'Daily Rate', 'Phone'])
        
        for emp in employees:
            writer.writerow([emp.name, emp.role, emp.daily_rate, emp.phone])
        
        output.seek(0)
        return Response({
            "data": output.getvalue(),
            "message": "Employees exported successfully"
        }, status=status.HTTP_200_OK)