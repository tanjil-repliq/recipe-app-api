"""
Views for create user API
"""

from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user to system"""

    serializer_class = UserSerializer
