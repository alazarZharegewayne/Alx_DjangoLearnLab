from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .serializers import UserSerializer, BookSerializer
from .models import Book

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    User registration endpoint
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create token for the new user
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ... rest of your existing views ...
