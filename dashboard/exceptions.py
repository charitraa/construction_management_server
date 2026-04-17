"""
Custom exceptions for dashboard management that maintain consistent API response format.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class DashboardManagementException(APIException):
    """
    Base exception for dashboard management operations.
    Maintains consistent API response format: {message, data}
    """

    status_code = 400
    default_detail = "An error occurred in dashboard management."

    def __init__(self, message=None, status_code=None):
        self.detail = message or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.detail)


class DashboardDataNotFoundException(DashboardManagementException):
    """Exception when dashboard data is not found."""

    status_code = 404
    default_detail = "Dashboard data not found."


class DashboardCalculationException(DashboardManagementException):
    """Exception when dashboard calculation fails."""

    status_code = 400
    default_detail = "Failed to calculate dashboard statistics. Please check your input."
