from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .exceptions import SerializerValidationError
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required fields.
    """
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "password",
            "confirm_password",
            "is_active"
            ]


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise SerializerValidationError("Passwords do not match.")

        if len(attrs['password']) < 8:
            raise SerializerValidationError("Password must be at least 8 characters long.")

        try:
            validate_password(attrs['password'])
        except Exception as e:
            raise SerializerValidationError(str(e))

        email = attrs['email'].lower()
        if User.objects.filter(email=email).exists():
            raise SerializerValidationError("A user with this email already exists.")

        attrs['email'] = email
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            is_active=validated_data['is_active']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details, including role and page information."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "is_active",
            "is_superuser",
            "is_staff",
            "date_joined"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user details, allowing partial updates."""

   
    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active"
            ]

    def validate_email(self, value):
        """Ensure email is unique when updating."""
        user = self.instance
        if User.objects.filter(email=value.lower()).exclude(id=user.id).exists():
            raise SerializerValidationError("This email is already in use."
            )
        return value.lower()
    def update(self, instance, validated_data):
        """Update user details and handle role/page changes."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user password."""
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'new_password_confirm']

    def validate(self, attrs):
        """Validate password and confirm password match."""
        user = self.instance

        if not user.check_password(attrs['current_password']):
            raise SerializerValidationError({"Current password is incorrect."})
        
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise SerializerValidationError({"New passwords do not match."})
        
        validate_password(attrs['new_password'])
        
        return attrs

    def update(self, instance, validated_data):
        """Update the user's password."""
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

