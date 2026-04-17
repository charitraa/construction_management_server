from django.urls import path
from .views import  UserDestroyView, UserUpdateView, LoginView, UserCreateView, UserListView, UserProfileView, LogoutView, UserRetrieveView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('details/update/', UserUpdateView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('details/', UserListView.as_view(), name='user-detail'),
    path('me/', UserProfileView.as_view(), name='user-me'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('details/<str:user_id>/', UserRetrieveView.as_view(), name='user-detail-by-id'),
    path('delete/<str:user_id>/', UserDestroyView.as_view(), name='user-delete'),
]
