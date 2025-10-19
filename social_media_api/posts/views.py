from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer,
    LikeSerializer
)
from notifications.utils import create_like_notification, create_comment_notification

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = serializer.save(post=post, author=request.user)
            
            # Create notification if the post author is not the commenter
            if post.author != request.user:
                create_comment_notification(post.author, request.user, post)
            
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments.
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Like a post
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user already liked the post
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response(
            {'error': 'You have already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create like
    like = Like.objects.create(user=request.user, post=post)
    
    # Create notification if the post author is not the liker
    if post.author != request.user:
        create_like_notification(post.author, request.user, post)
    
    serializer = LikeSerializer(like)
    return Response({
        'message': 'Post liked successfully',
        'like': serializer.data,
        'likes_count': post.likes_count
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Unlike a post
    """
    post = get_object_or_404(Post, pk=pk)
    
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        
        return Response({
            'message': 'Post unliked successfully',
            'likes_count': post.likes_count
        }, status=status.HTTP_200_OK)
        
    except Like.DoesNotExist:
        return Response(
            {'error': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def post_likes(request, pk):
    """
    Get all likes for a post
    """
    post = get_object_or_404(Post, pk=pk)
    likes = post.likes.all()
    serializer = LikeSerializer(likes, many=True)
    
    return Response({
        'post': post.title,
        'likes': serializer.data,
        'count': likes.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get feed of posts from users that the current user follows
    """
    # Get users that the current user follows
    following_users = request.user.following.all()
    
    # Get posts from followed users, ordered by most recent first
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Add pagination
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(posts, request)
    
    serializer = PostSerializer(result_page, many=True, context={'request': request})
    
    return paginator.get_paginated_response(serializer.data)