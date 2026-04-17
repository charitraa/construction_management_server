"""
Custom exceptions for payroll management that maintain consistent API response format.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class PayrollManagementException(APIException):
    """
    Base exception for payroll management operations.
    Maintains consistent API response format: {message, data}
    """

    status_code = 400
    default_detail = "An error occurred in payroll management."

    def __init__(self, message=None, status_code=None):
        self.detail = message or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.detail)


class PayrollNotFoundException(PayrollManagementException):
    """Exception when payroll data is not found."""

    status_code = 404
    default_detail = "Payroll data not found."


class PayrollCalculationException(PayrollManagementException):
    """Exception when payroll calculation fails."""

    status_code = 400
    default_detail = "Failed to calculate payroll. Please check your input."


class InvalidPayrollDataException(PayrollManagementException):
    """Exception when payroll data is invalid."""

    status_code = 400
    default_detail = "Invalid payroll data provided."


class InvalidMonthException(PayrollManagementException):
    """Exception when month parameter is invalid."""

    status_code = 400
    default_detail = "Invalid month format. Please use YYYY-MM format."
