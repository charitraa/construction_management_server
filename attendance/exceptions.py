"""
Custom exceptions for attendance management that maintain consistent API response format.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class AttendanceManagementException(APIException):
    """
    Base exception for attendance management operations.
    Maintains consistent API response format: {message, data}
    """

    status_code = 400
    default_detail = "An error occurred in attendance management."

    def __init__(self, message=None, status_code=None):
        self.detail = message or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.detail)


class AttendanceNotFoundException(AttendanceManagementException):
    """Exception when attendance record is not found."""

    status_code = 404
    default_detail = "Attendance record not found."


class AttendanceAlreadyExistsException(AttendanceManagementException):
    """Exception when attendance already exists for employee on date."""

    status_code = 400
    default_detail = "Attendance already exists for this employee on this date."


class AttendanceCreationException(AttendanceManagementException):
    """Exception when attendance creation fails."""

    status_code = 400
    default_detail = "Failed to create attendance record. Please check your input."


class AttendanceUpdateException(AttendanceManagementException):
    """Exception when attendance update fails."""

    status_code = 400
    default_detail = "Failed to update attendance record. Please check your input."


class AttendanceDeleteException(AttendanceManagementException):
    """Exception when attendance deletion fails."""

    status_code = 400
    default_detail = "Failed to delete attendance record."


class InvalidAttendanceDataException(AttendanceManagementException):
    """Exception when attendance data is invalid."""

    status_code = 400
    default_detail = "Invalid attendance data provided."
