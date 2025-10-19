from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add feed endpoint
    path('feed/', views.user_feed, name='user-feed'),
    # Like endpoints
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
    path('posts/<int:pk>/likes/', views.post_likes, name='post-likes'),
]