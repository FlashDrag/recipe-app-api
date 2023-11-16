"""
Views for the user API
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample
)

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


@extend_schema_view(
    post=extend_schema(
        summary='Create a new user',
        description='Create a new user in the system.',
        examples=[
            OpenApiExample(
                'Create a new user',
                summary='Return the created user',
                description='Return the created user with the auth token',
                value={
                    'email': 'user@example.com',
                    'name': 'string',
                    'token': 'string',
                },
                response_only=True,
            ),
        ],
    ),
)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        response_data = serializer.data
        response_data['token'] = token.key
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


@extend_schema_view(
    post=extend_schema(
        summary='Create a new auth token',
        description='Get or create a new auth token for the user.',
        examples=[
            OpenApiExample(
                'Create a new auth token',
                summary='Return the created auth token',
                description='Return the created auth token for the user',
                value={
                    'token': 'string',
                },
                response_only=True,
            ),
        ],
    ),
)
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
