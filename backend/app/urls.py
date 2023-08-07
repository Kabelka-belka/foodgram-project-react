from django.urls import include, path
from rest_framework import routers

from .views import (
    index, TagViewSet, RecipeWiewSet, IngredientViewSet, CustomUserViewSet,
    FollowMixin, FollowListMixin)


router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeWiewSet)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    RecipeWiewSet,
    basename='shopping_cart')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    RecipeWiewSet,
    basename='favorite')
router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients')
router_v1.register(r'(?P<user_id>\d+)/subscribe',
                   FollowMixin,
                   basename='subscribe')
router_v1.register('subscriptions',
                   FollowListMixin,
                   basename='subscriptions')
router_v1.register('', CustomUserViewSet)

urlpatterns = [
    path('index', index),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
