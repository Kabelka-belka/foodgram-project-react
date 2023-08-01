from django.db.models import Sum
from django.http.response import HttpResponse
from rest_framework import (
    filters, permissions, status, viewsets)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import (
    Tag, Recipe, ShoppingCart, Favorite, 
    Ingredient, IngredientToRecipe)
from .serializers import (
    RecipeCreateSerializer, ShoppingCartSerializer,
    FavoriteSerializer, IngredientSerializer, TegSerializer,
    RecipeReadSerializer)
from .permissions import AuthorIsRequestUserPermission
from .filters import MyFilterSet, IngredientFilter
from .pagination import CustomPagination

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение одного ингредиента или списка"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение одного тега или списка"""

    queryset = Tag.objects.all()
    serializer_class = TegSerializer


class RecipeWiewSet(viewsets.ModelViewSet):
    """Отображение и создание рецептов"""

    permission_classes = (AuthorIsRequestUserPermission, )
    queryset = Recipe.objects.all()
    filter_class = MyFilterSet
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.save(Favorite, request.user, pk)
        return self.remove(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.save(ShoppingCart, request.user, pk)
        return self.remove(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        """ Скачивает список покупок. """
        ingredients = IngredientToRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))
        return self.send_message(ingredients)

    def save(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'The recipe has been added!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        obj = model.objects.create(user=user, recipe=recipe)
        if self.shopping_cart:
            serializer = ShoppingCartSerializer(obj)
        elif self.favorite:
            serializer = FavoriteSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def remove(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response({'message':
                             'The recipe has been successfully deleted.'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'The recipe has been deleted!'},
                        status=status.HTTP_400_BAD_REQUEST)
