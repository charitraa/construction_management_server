from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from core.permission import LoginRequiredPermission
from core.throttling import LoginRateThrottle
from .serializers import  UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .services import UserService

class LoginView(TokenObtainPairView):
    """ View for user login that returns JWT tokens and user data. """
    # Apply strict rate limiting to prevent brute force attacks
    throttle_classes = [LoginRateThrottle]
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        data = UserService.login_user(email, password)

        if data:
            response = Response({
                "message": "Login successful",
                "data": {
                        "user": UserSerializer(data["user"]).data,
                        "access": data["access"],
                        "refresh": data["refresh"]
                        },
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key="access_token",
                value=data["access"],
                httponly=True,
                secure=True,
                samesite="None"
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=True,
                samesite="None"
            )
            return response

        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    """ Admin-only view to retrieve all user details. """
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        data = UserService.get_all_users()
        return Response({ "data": UserSerializer(data, many=True).data, "message": "User details retrieved successfully"}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    """ View to retrieve user details for the authenticated user. """
    permission_classes = [LoginRequiredPermission]

    def get(self, request, *args, **kwargs):
        data = UserService.get_user_me(request.user)
        return Response({"data": data, "message": "User details retrieved successfully"}, status=status.HTTP_200_OK)

class UserRetrieveView(APIView):
    """ Admin-only view to retrieve user details by ID. """
    permission_classes = [LoginRequiredPermission]

    def get(self, user_id, *args, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"data": UserSerializer(user).data, "message": "User details retrieved successfully"}, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    """Admin-only view to update user details."""

    permission_classes = [LoginRequiredPermission]
    def put(self, request, user_id, *args, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class UserCreateView(APIView):
    """Admin-only view to create new users."""

    permission_classes = [LoginRequiredPermission]
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"data": UserSerializer(user).data, "message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class UserDestroyView(APIView):
    """Admin-only view to delete a user."""

    permission_classes = [LoginRequiredPermission]
    def delete(self, user_id, *args, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        UserService.delete_user(user)
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    """Logs out the user by deleting the JWT cookies."""

    permission_classes = [LoginRequiredPermission]
    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("access_token", path="/", samesite="None")
        response.delete_cookie("refresh_token", path="/", samesite="None")
        return response