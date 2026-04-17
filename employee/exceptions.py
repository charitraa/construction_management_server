"""
Custom exceptions for employee management that maintain consistent API response format.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class EmployeeManagementException(APIException):
    """
    Base exception for employee management operations.
    Maintains consistent API response format: {message, data}
    """

    status_code = 400
    default_detail = "An error occurred in employee management."

    def __init__(self, message=None, status_code=None):
        self.detail = message or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.detail)


class EmployeeNotFoundException(EmployeeManagementException):
    """Exception when employee is not found."""

    status_code = 404
    default_detail = "Employee not found."


class EmployeeAlreadyExistsException(EmployeeManagementException):
    """Exception when employee already exists."""

    status_code = 400
    default_detail = "An employee with this information already exists."


class EmployeeCreationException(EmployeeManagementException):
    """Exception when employee creation fails."""

    status_code = 400
    default_detail = "Failed to create employee. Please check your input."


class EmployeeUpdateException(EmployeeManagementException):
    """Exception when employee update fails."""

    status_code = 400
    default_detail = "Failed to update employee. Please check your input."


class EmployeeDeleteException(EmployeeManagementException):
    """Exception when employee deletion fails."""

    status_code = 400
    default_detail = "Failed to delete employee."


class InvalidEmployeeDataException(EmployeeManagementException):
    """Exception when employee data is invalid."""

    status_code = 400
    default_detail = "Invalid employee data provided."