# repository.py
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserRepository:
    """Repository class for handling all database interactions related to the User model."""
    @staticmethod
    def get_all():
        return User.objects.select_related("role").prefetch_related("pages")
    
    @staticmethod
    def get_by_id(user_id):
     return User.objects.filter(id=user_id).first()
    
    @staticmethod
    def authenticate_user(email, password):
        return authenticate(email=email, password=password)
    
    @staticmethod
    def delete_user(user):
        user.delete()