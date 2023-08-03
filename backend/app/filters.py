import django_filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag, Ingredient


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов. """

    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class MyFilterSet(django_filters.rest_framework.FilterSet):
    """Фильтр для рецептов. """

    author = django_filters.rest_framework.NumberFilter(
        field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_shopping_cart')

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(infavorite__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
