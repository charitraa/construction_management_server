from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed, PermissionDenied, Throttled
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

logger = logging.getLogger("django")  # Uses same logging config

def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent API response format.
    All responses follow the pattern: {message, data, status_code}
    """
    response = exception_handler(exc, context)

    # Log full exception details for debugging (not exposed to users)
    logger.error(
        "API Exception occurred",
        extra={
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "request_method": context['request'].method,
            "request_path": context['request'].path,
            "user": getattr(context['request'].user, 'pk', None) if hasattr(context['request'], 'user') else None
        },
        exc_info=True
    )

    if response is None:
        # Unhandled server errors - provide generic message
        logger.error("Unhandled server error", exc_info=exc, stack_info=True)
        return Response(
            {
                "message": "An unexpected error occurred. Please try again later.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Handle Django ValidationErrors (from models/forms)
    if isinstance(exc, DjangoValidationError):
        # Convert Django ValidationErrors to consistent API format
        if hasattr(exc, 'message_dict'):
            # Field-specific errors: {"field": ["error message"]}
            error_dict = exc.message_dict
            messages = []

            # Flatten error messages
            for field, errors in error_dict.items():
                if isinstance(errors, list):
                    for error in errors:
                        messages.append(f"{field}: {error}")
                else:
                    messages.append(f"{field}: {errors}")

            response.data = {
                "message": "Validation failed. Please check your input.",
                "data": messages,
                "status_code": status.HTTP_400_BAD_REQUEST
            }
        elif hasattr(exc, 'messages'):
            # General errors: ["error message"]
            response.data = {
                "message": ". ".join(exc.messages),
                "status_code": status.HTTP_400_BAD_REQUEST
            }
        else:
            # Simple error message
            response.data = {
                "message": str(exc),
                "status_code": status.HTTP_400_BAD_REQUEST
            }
        return response

    # Handle specific exception types with appropriate messages
    if isinstance(exc, Throttled):
        # Rate limit exceeded - already has user-friendly message from throttling
        if isinstance(response.data, dict):
            # Custom throttling format already provides good messages
            pass
        else:
            response.data = {
                "message": "Too many requests. Please slow down and try again later.",
                "status_code": status.HTTP_429_TOO_MANY_REQUESTS
            }
        return response

    if isinstance(exc, AuthenticationFailed):
        # Authentication failed - generic message to prevent account enumeration
        response.data = {
            "message": "Authentication failed. Please check your credentials and try again.",
            "status_code": status.HTTP_401_UNAUTHORIZED
        }
        return response

    if isinstance(exc, PermissionDenied):
        # Permission denied - generic message
        response.data = {
            "message": "You do not have permission to perform this action.",
            "status_code": status.HTTP_403_FORBIDDEN
        }
        return response

    # Standardize response format for APIExceptions
    if isinstance(exc, APIException):
        # Custom API exceptions (like UserManagementException)
        if isinstance(response.data, dict):
            # Already in dict format, ensure consistent structure
            if "message" not in response.data and "detail" in response.data:
                response.data["message"] = response.data.pop("detail")

            # Add status_code if not present
            if "status_code" not in response.data:
                response.data["status_code"] = response.status_code

            # Remove sensitive information
            response.data = sanitize_error_data(response.data)
        elif isinstance(response.data, list):
            # Handle list-based error responses
            response.data = {
                "message": "Validation failed. Please check your input.",
                "data": response.data,
                "status_code": response.status_code
            }
        else:
            # String error message
            response.data = {
                "message": str(response.data),
                "status_code": response.status_code
            }

    return response


def sanitize_error_data(data):
    """
    Remove potentially sensitive information from error responses.
    This prevents information disclosure while maintaining useful feedback.
    """
    if not isinstance(data, dict):
        return data

    sensitive_keys = [
        'traceback', 'stack_trace', 'debug', 'error_details',
        'internal_error', 'server_error', 'exception', 'exception_type',
        'file_path', 'line_number', 'function', 'module'
    ]

    sanitized = {}
    for key, value in data.items():
        # Skip sensitive keys
        if key.lower() in [k.lower() for k in sensitive_keys]:
            continue

        # Sanitize nested dictionaries
        if isinstance(value, dict):
            sanitized[key] = sanitize_error_data(value)
        # Sanitize lists (often contain field errors)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_list_item(item) for item in value]
        # Sanitize string values that might contain sensitive info
        elif isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        else:
            sanitized[key] = value

    return sanitized


def sanitize_list_item(item):
    """Sanitize individual items in error lists."""
    if isinstance(item, dict):
        return sanitize_error_data(item)
    elif isinstance(item, str):
        return sanitize_string(item)
    return item


def sanitize_string(text):
    """
    Remove potentially sensitive information from error strings.
    Preserves useful error messages while removing paths, emails, etc.
    """
    import re

    # Remove file paths (both Unix and Windows formats)
    text = re.sub(r'[/\\][a-zA-Z0-9_\-/.\\]+[/\\][a-zA-Z0-9_\-/.\\]+\.(py|js|html|css|json|txt)', '[file]', text)

    # Remove email addresses
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[email]', text)

    # Remove IP addresses
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)
    text = re.sub(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b', '[IPv6]', text)

    # Remove database connection strings
    text = re.sub(r'postgres://[^:@]+:[^@]+@[^/]+', '[database_connection]', text)
    text = re.sub(r'mysql://[^:@]+:[^@]+@[^/]+', '[database_connection]', text)

    # Remove secret keys/patterns (but keep legitimate error messages)
    text = re.sub(r'[A-Za-z0-9]{40,}', '[key]', text)  # Long alphanumeric strings

    return text
