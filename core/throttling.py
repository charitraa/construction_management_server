"""
Custom throttling classes for API rate limiting.
Provides environment-specific rate limits for different endpoint types.
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.cache import cache
from django.conf import settings
from rest_framework.exceptions import Throttled
import time


class AuthenticationRateThrottle(AnonRateThrottle):
    """
    Strict rate limiting for authentication endpoints to prevent brute force attacks.
    Applied to login, password reset, and other authentication-sensitive endpoints.
    """

    # Default rates - will be overridden by settings
    scope = 'auth'
    rate = '5/min'  # 5 attempts per minute by default

    def get_cache_key(self, request, view):
        """
        Generate cache key for rate limiting based on IP address.
        This prevents brute force attacks from single IP addresses.
        """
        # Use IP address for anonymous users (most authentication attempts)
        ident = self.get_ident(request)

        return f'auth_throttle_{ident}'

    def throttle_failure(self):
        """
        Override to provide more detailed error messages.
        """
        wait = self.wait()

        # Provide user-friendly error message
        raise Throttled(
            detail={
                "message": "Too many authentication attempts. Please try again later.",
                "retry_after": f"{int(wait)} seconds"
            }
        )


class StrictAnonRateThrottle(AnonRateThrottle):
    """
    Strict rate limiting for anonymous users to prevent abuse.
    """

    scope = 'anon_strict'
    rate = '100/hour'  # 100 requests per hour for anonymous users

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return f'anon_strict_{ident}'


class StrictUserRateThrottle(UserRateThrottle):
    """
    Strict rate limiting for authenticated users to prevent API abuse.
    """

    scope = 'user_strict'
    rate = '1000/hour'  # 1000 requests per hour for authenticated users

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'user_strict_{ident}'


class BurstRateThrottle(AnonRateThrottle):
    """
    Burst rate limiting to prevent denial-of-service attacks.
    Allows short bursts but restricts sustained high traffic.
    """

    scope = 'burst'
    rate = '20/min'  # 20 requests per minute (burst protection)

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return f'burst_{ident}'


class LoginRateThrottle(AuthenticationRateThrottle):
    """
    Specific throttle for login endpoint with extra account lockout protection.
    """

    scope = 'login'
    LOCKOUT_THRESHOLD = 5  # Number of failed attempts before lockout
    LOCKOUT_DURATION = 15 * 60  # 15 minutes lockout

    def __init__(self):
        super().__init__()
        self.lockout_cache_prefix = 'login_lockout_'

    def get_cache_key(self, request, view):
        """Generate cache key including account lockout status."""
        ident = self.get_ident(request)

        # Check if IP is locked out
        lockout_key = f'{self.lockout_cache_prefix}{ident}'
        if cache.get(lockout_key):
            # IP is locked out, return lockout key
            return lockout_key

        # Not locked out, return normal throttle key
        return f'login_throttle_{ident}'

    def throttle_failure(self):
        """
        Override to implement account lockout on repeated failures.
        """
        ident = self.get_ident(request=None)  # Get identifier
        lockout_key = f'{self.lockout_cache_prefix}{ident}'

        # Check if already locked out
        if cache.get(lockout_key):
            wait = cache.ttl(lockout_key)
            raise Throttled(
                detail={
                    "message": "Your IP has been temporarily locked due to too many failed login attempts.",
                    "retry_after": f"{wait} seconds"
                }
            )

        # Count recent failures to determine if lockout is needed
        throttle_key = f'login_throttle_{ident}'
        failure_count = cache.get(f'{throttle_key}_count', 0)

        if failure_count >= self.LOCKOUT_THRESHOLD:
            # Lockout this IP
            cache.set(lockout_key, True, self.LOCKOUT_DURATION)
            raise Throttled(
                detail={
                    "message": "Too many failed login attempts. Your IP has been temporarily locked.",
                    "retry_after": f"{self.LOCKOUT_DURATION} seconds"
                }
            )

        # Normal throttling
        wait = self.wait()
        raise Throttled(
            detail={
                "message": "Too many login attempts. Please wait before trying again.",
                "retry_after": f"{int(wait)} seconds"
            }
        )


class PasswordResetRateThrottle(AuthenticationRateThrottle):
    """
    Specific throttle for password reset endpoints to prevent abuse.
    """

    scope = 'password_reset'
    rate = '3/hour'  # 3 password reset attempts per hour

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return f'password_reset_{ident}'


class DataModificationRateThrottle(UserRateThrottle):
    """
    Rate limiting for data modification endpoints (POST, PUT, DELETE).
    More restrictive than general endpoints.
    """

    scope = 'data_modification'
    rate = '100/minute'  # 100 modification requests per minute

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'data_mod_{ident}'


class UploadRateThrottle(UserRateThrottle):
    """
    Rate limiting for file upload endpoints.
    Prevents abuse of upload functionality.
    """

    scope = 'upload'
    rate = '10/minute'  # 10 upload operations per minute

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'upload_{ident}'


def get_throttle_classes(request_method):
    """
    Returns appropriate throttle classes based on request method.
    More restrictive for POST/PUT/DELETE operations.
    """

    if request_method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        return [DataModificationRateThrottle]
    else:
        return [StrictUserRateThrottle]


class EnvironmentBasedThrottleMixin:
    """
    Mixin to adjust throttle rates based on environment.
    More lenient in development, strict in production.
    """

    def get_rate(self):
        """Get rate limit based on environment."""
        environment = getattr(settings, 'ENVIRONMENT', 'development')

        # Default rates (can be overridden in settings)
        rates = {
            'auth': {
                'development': '20/min',
                'production': '5/min'
            },
            'anon_strict': {
                'development': '500/hour',
                'production': '100/hour'
            },
            'user_strict': {
                'development': '2000/hour',
                'production': '1000/hour'
            },
            'burst': {
                'development': '60/min',
                'production': '20/min'
            },
            'password_reset': {
                'development': '10/hour',
                'production': '3/hour'
            },
            'data_modification': {
                'development': '200/minute',
                'production': '100/minute'
            },
            'upload': {
                'development': '30/minute',
                'production': '10/minute'
            }
        }

        scope_rates = rates.get(self.scope, {})
        return scope_rates.get(environment, self.rate)
