from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings

class AllowOptionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin", "")

            # Only allow CORS requests from whitelisted origins
            allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])

            if origin in allowed_origins:
                response = HttpResponse()
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
                response["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "Content-Type, Authorization")
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Max-Age"] = "86400"  # Cache for 24 hours
                return response
            else:
                # Return forbidden for unauthorized origins
                return HttpResponse(status=403)
        return None
class RefreshTokenMiddleware:
    """Middleware to handle JWT token refresh securely."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Process request and set new access token if needed."""
        try:
            response = self.get_response(request)

            if hasattr(request, "new_access_token"):
                # Use environment-specific SameSite setting
                samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')
                secure = getattr(settings, 'SESSION_COOKIE_SECURE', True)

                response.set_cookie(
                    key="access_token",
                    value=request.new_access_token,
                    httponly=True,
                    secure=secure,
                    samesite=samesite
                )

            return response
        except Exception as e:
            # Log error but don't expose details to users
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in RefreshTokenMiddleware: {str(e)}", exc_info=True)

            # Return original response even if token refresh fails
            return self.get_response(request)