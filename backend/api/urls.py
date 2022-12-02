from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.views import (UserSignUpAndView, UserProfileView,
                       MeUserProfileView, UserSetPasswordView,
                       GetIngredientsViewSet, GetTagsViewSet,
                       RecipesViewSet, UserSubscriptionsView, AddSubView,
                       RecipeInFavoriteView, RecipeInShoppingCartView,
                       LoadShoppingCart)


router = SimpleRouter()
router.register('ingredients', GetIngredientsViewSet)
router.register('tags', GetTagsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('users/', UserSignUpAndView.as_view()),
    path('users/<int:pk>/', UserProfileView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/', MeUserProfileView.as_view()),
    path('users/set_password/', UserSetPasswordView.as_view()),
    path('users/subscriptions/', UserSubscriptionsView.as_view()),
    path('users/<int:pk>/subscribe/', AddSubView.as_view()),
    path('recipes/<int:pk>/favorite/', RecipeInFavoriteView.as_view()),
    path('recipes/<int:pk>/shopping_cart/',
         RecipeInShoppingCartView.as_view()),
    path('recipes/download_shopping_cart/', LoadShoppingCart.as_view()),
    path('', include(router.urls)),
]
