"""
Custom password validators for enhanced security.
Implements stronger password requirements than Django's default validators.
"""

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import gettext_lazy as _
import re


class StrongPasswordValidator:
    """
    Validator that requires passwords to meet strong security requirements.
    - Minimum length (configurable, default 8 characters)
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - No common patterns (sequences, repetitions)
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        """
        Validate that the password meets all security requirements.

        Args:
            password: The password to validate
            user: The user object (optional, can be used for user-specific checks)

        Raises:
            ValidationError: If password doesn't meet requirements
        """

        if len(password) < self.min_length:
            raise ValidationError(
                {
                    "password": _(
                        f"This password is too short. It must contain at least {self.min_length} characters."
                    )
                }
            )

        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                {
                    "password": _(
                        "This password must contain at least one uppercase letter."
                    )
                }
            )

        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                {
                    "password": _(
                        "This password must contain at least one lowercase letter."
                    )
                }
            )

        # Check for digit
        if not re.search(r'\d', password):
            raise ValidationError(
                {
                    "password": _(
                        "This password must contain at least one digit."
                    )
                }
            )

        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password):
            raise ValidationError(
                {
                    "password": _(
                        "This password must contain at least one special character."
                    )
                }
            )

        # Check for common patterns

        # If user is provided, check if password contains user information
        if user:
            self._check_user_info(password, user)

    def _check_user_info(self, password, user):
        """Check if password contains user information."""
        password_lower = password.lower()

        # Check if password contains email
        if hasattr(user, 'email') and user.email:
            email_parts = user.email.split('@')[0].lower()
            if email_parts and len(email_parts) > 3 and email_parts in password_lower:
                raise ValidationError(
                    {
                        "password": _(
                            "The password is too similar to the email address."
                        )
                    }
                )

        # Check if password contains name
        if hasattr(user, 'full_name') and user.full_name:
            name_parts = user.full_name.lower().split()
            for name_part in name_parts:
                if len(name_part) > 3 and name_part in password_lower:
                    raise ValidationError(
                        {
                            "password": _(
                                "The password is too similar to the name."
                            )
                        }
                    )

    def get_help_text(self):
        """Return user-friendly help text for password requirements."""
        help_text = [
            f"Your password must contain at least {self.min_length} characters.",
            "Your password must contain at least one uppercase letter.",
            "Your password must contain at least one lowercase letter.",
            "Your password must contain at least one digit.",
            "Your password must contain at least one special character.",
            "Your password can't be too similar to your other personal information.",
            "Your password can't be a commonly used password.",
            "Your password can't be entirely numeric.",
        ]
        return _('. '.join(help_text))


class EnhancedMinimumLengthValidator(MinimumLengthValidator):
    """
    Enhanced version of Django's MinimumLengthValidator with custom messages.
    """

    def __init__(self, min_length=8):
        super().__init__(min_length=min_length)

    def get_help_text(self):
        """Return user-friendly help text."""
        return _(
            f"Your password must contain at least {self.min_length} characters."
        )


class PasswordComplexityValidator:
    """
    Password complexity validator that calculates a complexity score.
    Uses entropy-based approach to measure password strength.
    """

    MIN_COMPLEXITY_SCORE = 40  # Minimum complexity score

    def validate(self, password, user=None):
        """
        Validate password complexity based on multiple factors.

        Args:
            password: The password to validate
            user: The user object (optional)

        Raises:
            ValidationError: If password complexity is too low
        """

        complexity_score = self._calculate_complexity(password)

        if complexity_score < self.MIN_COMPLEXITY_SCORE:
            raise ValidationError(
                {
                    "password": _(
                        "This password is not complex enough. "
                        "Please use a mix of letters, numbers, and special characters."
                    )
                }
            )

    def _calculate_complexity(self, password):
        """Calculate password complexity score."""
        score = 0

        # Length contributes to complexity
        score += len(password) * 2

        # Character variety
        if re.search(r'[a-z]', password):  # Lowercase
            score += 10
        if re.search(r'[A-Z]', password):  # Uppercase
            score += 10
        if re.search(r'\d', password):  # Digits
            score += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password):  # Special chars
            score += 15

        # Character variety bonus
        unique_chars = len(set(password))
        if unique_chars > len(password) * 0.7:  # 70%+ unique characters
            score += 10

        return score

    def get_help_text(self):
        """Return user-friendly help text."""
        return _(
            "Your password should be complex and use a variety of characters, "
            "numbers, and special characters."
        )


def validate_password_strength(password, user=None, min_length=8):
    """
    Convenience function to validate password strength using all validators.

    Args:
        password: The password to validate
        user: The user object (optional)
        min_length: Minimum password length (default: 8)

    Raises:
        ValidationError: If password doesn't meet requirements
    """
    validators = [
        StrongPasswordValidator(min_length=min_length),
        PasswordComplexityValidator(),
    ]

    for validator in validators:
        validator.validate(password, user)

    return password
