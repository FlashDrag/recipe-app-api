"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


# Allows to add descriptions to the API views in the Swagger UI
@extend_schema_view(
    list=extend_schema(
        summary='Retrieve a list of recipes',
        description='Retrieve a list of recipes for the authenticated user.',
    ),
    create=extend_schema(
        summary='Create a new recipe',
        description='Create a new recipe for the authenticated user.',
    ),
    retrieve=extend_schema(
        summary='Retrieve a recipe detail',
        description='Retrieve a recipe detail for the authenticated user.',
    ),
    update=extend_schema(
        summary='Update a recipe',
        description='Update a recipe for the authenticated user.',
    ),
    partial_update=extend_schema(
        summary='Partially update a recipe',
        description='Partially update a recipe for the authenticated user.',
    ),
    destroy=extend_schema(
        summary='Delete a recipe',
        description='Delete a recipe for the authenticated user.',
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
