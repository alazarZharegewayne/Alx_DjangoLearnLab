from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, UserUpdateSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    Returns token upon successful registration.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        # Get the token that was created in the serializer
        token = Token.objects.get(user=user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'token': token.key,
                'message': 'User registered successfully'
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_view(request):
    """
    View for user login.
    Returns token upon successful authentication.
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        
        return Response(
            {
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'token': token.key,
                'message': 'Login successful'
            },
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserProfileDetailView(generics.RetrieveAPIView):
    """
    View for retrieving public user profile information.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    """
    Follow a user
    """
    user_to_follow = get_object_or_404(CustomUser, username=username)
    
    if request.user == user_to_follow:
        return Response(
            {'error': 'You cannot follow yourself'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if user_to_follow in request.user.following.all():
        return Response(
            {'error': 'You are already following this user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Add to following
    request.user.following.add(user_to_follow)
    
    return Response({
        'message': f'You are now following {username}',
        'user': UserProfileSerializer(user_to_follow, context={'request': request}).data,
        'is_following': True,
        'followers_count': user_to_follow.followers_count,
        'following_count': request.user.following_count
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, username):
    """
    Unfollow a user
    """
    user_to_unfollow = get_object_or_404(CustomUser, username=username)
    
    if request.user == user_to_unfollow:
        return Response(
            {'error': 'You cannot unfollow yourself'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if user_to_unfollow not in request.user.following.all():
        return Response(
            {'error': 'You are not following this user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Remove from following
    request.user.following.remove(user_to_unfollow)
    
    return Response({
        'message': f'You have unfollowed {username}',
        'user': UserProfileSerializer(user_to_unfollow, context={'request': request}).data,
        'is_following': False,
        'followers_count': user_to_unfollow.followers_count,
        'following_count': request.user.following_count
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    """
    Get list of users that the current user is following
    """
    following_users = request.user.following.all()
    serializer = UserProfileSerializer(following_users, many=True, context={'request': request})
    
    return Response({
        'following': serializer.data,
        'count': following_users.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request):
    """
    Get list of users who follow the current user
    """
    followers = request.user.followers.all()
    serializer = UserProfileSerializer(followers, many=True, context={'request': request})
    
    return Response({
        'followers': serializer.data,
        'count': followers.count()
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    View for user logout (delete token).
    """
    try:
        # Delete the token to logout
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Error during logout'}, 
            status=status.HTTP_400_BAD_REQUEST
        )