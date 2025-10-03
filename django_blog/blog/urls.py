from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post URLs
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('posts/new/', views.post_create, name='post-create'),
    path('posts/<int:pk>/edit/', views.post_update, name='post-update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post-delete'),
]
