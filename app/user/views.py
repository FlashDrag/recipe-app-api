"""
Views for the user API
"""
from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# Allows to add descriptions to the API views in the Swagger UI
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve User',
        description='Retrieve and return the authenticated user.'
    ),
    put=extend_schema(
        summary='Update User',
        description='Update the authenticated user\'s information.'
    ),
    patch=extend_schema(
        summary='Partially Update User',
        description='Partially update the authenticated user\'s information.'
    )
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
