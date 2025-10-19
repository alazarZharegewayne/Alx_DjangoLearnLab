from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    
    # Follow management endpoints
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow-user'),
    path('following/', views.following_list, name='following-list'),
    path('followers/', views.followers_list, name='followers-list'),
]