"""
Custom exceptions for user management that maintain consistent API response format.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class UserManagementException(APIException):
    """
    Base exception for user management operations.
    Maintains consistent API response format: {message, data}
    """

    status_code = 400
    default_detail = "An error occurred in user management."

    def __init__(self, message=None, status_code=None):
        """
        Initialize with custom message and optional status code.

        Args:
            message: Error message string
            status_code: HTTP status code (optional)
        """
        self.detail = message or self.default_detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=self.detail)


class EmailRequiredException(UserManagementException):
    """Exception when email is required but not provided."""

    status_code = 400
    default_detail = "The Email field must be set."


class SuperuserStaffException(UserManagementException):
    """Exception when superuser doesn't have is_staff=True."""

    status_code = 400
    default_detail = "Superuser must have is_staff=True."


class SuperuserSuperuserException(UserManagementException):
    """Exception when superuser doesn't have is_superuser=True."""

    status_code = 400
    default_detail = "Superuser must have is_superuser=True."


class UserCreationException(UserManagementException):
    """Exception when user creation fails."""

    status_code = 400
    default_detail = "Failed to create user. Please check your input."


class PasswordValidationException(UserManagementException):
    """Exception when password doesn't meet requirements."""

    status_code = 400
    default_detail = "Password does not meet security requirements."

class SerializerValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        self.detail = {"message": message}