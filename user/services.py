# services.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from .repository import  UserRepository
from .serializers import UserSerializer

class UserService:
    """Service class for handling business logic related to user operations."""
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return JWT tokens along with user data."""
        user = UserRepository.authenticate_user(email, password)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            serialized_user = UserSerializer(user).data
            return {
                "user": serialized_user,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        return None

    @staticmethod
    def get_all_users():
        """Retrieve all users from the database and cache them for 5 minutes."""
        return cache.get_or_set("user_all_details", UserRepository.get_all(), 60 * 5)

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user by their ID from the database."""
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def get_user_me(user):
        """ Retrieve user details for the authenticated user."""
        return UserSerializer(user).data

    @staticmethod
    def delete_user(user):
        """ Delete a user from the database and clear the cache."""
        cache.delete("user_all_details")
        UserRepository.delete_user(user)