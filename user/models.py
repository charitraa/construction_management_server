from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from .exceptions import (
    EmailRequiredException,
    SuperuserStaffException,
    SuperuserSuperuserException,
    UserCreationException
)

class UserManager(BaseUserManager):
    """Custom user manager to handle user creation and superuser creation."""
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        Raises custom exceptions for invalid data that maintain API response consistency.
        """
        if not email:
            raise EmailRequiredException()

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Set password if provided
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        try:
            user.save(using=self._db)
        except Exception as e:
            # Catch any database errors and convert to consistent format
            raise UserCreationException(
                message=f"Failed to create user: {str(e)}",
                status_code=400
            )

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        Raises custom exceptions for invalid data that maintain API response consistency.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise SuperuserStaffException()
        if extra_fields.get("is_superuser") is not True:
            raise SuperuserSuperuserException()

        return self.create_user(email, password, **extra_fields)   
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email as the unique identifier."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        name = f"{self.full_name}".strip()
        return name if name else self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)