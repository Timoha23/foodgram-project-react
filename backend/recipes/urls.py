from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (LoadShoppingCart, RecipeInFavoriteView,
                    RecipeInShoppingCartView, RecipesViewSet)

router = SimpleRouter()
router.register('', RecipesViewSet)

urlpatterns = [
    path('<int:pk>/favorite/', RecipeInFavoriteView.as_view()),
    path('<int:pk>/shopping_cart/',
         RecipeInShoppingCartView.as_view()),
    path('download_shopping_cart/', LoadShoppingCart.as_view()),
    path('', include(router.urls)),
]
