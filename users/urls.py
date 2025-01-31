from django.urls import path, include
from .views import RegisterView,LoginView,LogoutView,ListUsersView,UserDetailView,BlockUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('login',LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list/',ListUsersView.as_view(),name='users-list'),
    path('detail/<int:pk>',UserDetailView.as_view(),name='user-detail'),
    path('block/<int:user_id>',BlockUserView.as_view(),name='block-user'),
]