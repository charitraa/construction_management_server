from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class LoginRequiredPermission(BasePermission):
    """Custom permission class that checks for valid JWT tokens in cookies and refreshes them if necessary."""
    def has_permission(self, request, view):
        """Check for valid access token, and refresh if expired using refresh token."""
        auth = JWTAuthentication()
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        # if access token exists → try validating
        if access_token:
            try:
                validated_token = auth.get_validated_token(access_token)
                request.user = auth.get_user(validated_token)
                return True
            except Exception:
                pass  # Access token expired

        # Try refreshing using refresh token
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access = str(refresh.access_token)

                # Attach new access token to request
                validated_token = auth.get_validated_token(new_access)
                request.user = auth.get_user(validated_token)

                # Store new token in request for middleware to update cookie
                request.new_access_token = new_access

                return True
            except Exception:
                raise NotAuthenticated(detail="Session expired. Please login again.")

        raise NotAuthenticated(detail="Login required.")