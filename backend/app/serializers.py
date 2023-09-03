from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Follow, Ingredient, IngredientToRecipe, Recipe,
                     ShoppingCart, Tag, User)


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор регистрации юзера. """

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializer(UserSerializer):
    """Сериализатор отображения юзера. """

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            current_user = request.user

        return Follow.objects.filter(
            user=current_user.id,
            author=obj.id).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TegSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShortResipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для простого короткого отображения"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeFavoriteAndShopping(serializers.ModelSerializer):
    '''Recipe serializer for favorites and shopping list.'''

    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели соединяющей ингредиенты и рецепты"""

    id = serializers.IntegerField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientToRecipe
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецептов"""

    tags = TegSerializer(read_only=False, many=True)
    ingredients = IngredientToRecipeSerializer(
        many=True,
        source='ingredienttorecipe')
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
    read_only_fields = ('id', 'author', 'is_favorited',
                        'is_favorited')

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request:
            current_user = request.user
        return ShoppingCart.objects.filter(
            user=current_user.id,
            recipe=obj.id,
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request:
            current_user = request.user
        return Favorite.objects.filter(
            user=current_user.id,
            recipe=obj.id
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientToRecipeSerializer(
        many=True,
        source='ingredienttorecipe')
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, tags):
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальны')
            tags_list.append(tag)
            if len(tags_list) < 1:
                raise serializers.ValidationError(
                    'Отсуствуют теги')
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время готовки должно быть не меньше одной минуты')
        if cooking_time > 2880:
            raise serializers.ValidationError(
                'Время готовки должно быть не больше 2 суток')
        return cooking_time

    def validate_ingredients(self, data):
        if not data:
            raise serializers.ValidationError(
                'Отсутствуют ингредиенты!'
            )
        ingredients_list = []
        for ingredient in data:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Есть одинаковые ингредиенты!'
                )
            ingredients_list.append(ingredient_id)
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента больше 0')

        return data

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_liist = []
        for ingredient in ingredients:
            ingredient_liist.append(
                IngredientToRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
            )
        IngredientToRecipe.objects.bulk_create(ingredient_liist)

    def create(self, validated_data):
        request = self.context.get('request', None)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredienttorecipe')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientToRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredienttorecipe')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class FollowSerializer(CustomUserSerializer):
    """Сериализатор ингредиентов"""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            queryset = Recipe.objects.filter(
                author=obj).order_by('-id')[:int(limit)]
        else:
            queryset = Recipe.objects.filter(author=obj)

        return ShortResipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def create(self, validated_data):
        request = self.context.get('request')
        author_id = self.context.get('request').parser_context.get(
            'kwargs').get('user_id')

        current_user = request.user
        author = get_object_or_404(User, pk=author_id)
        Follow.objects.create(user=current_user, author=author)
        return author
