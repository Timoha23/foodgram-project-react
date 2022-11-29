from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.views import UserSignUpAndView, UserProfiles, UserProfile, UserSetPassword, GetIngredientsViewSet, GetTagsViewSet, RecipesViewSet, UserSubscriptions, AddSubView


router = SimpleRouter()
router.register('ingredients', GetIngredientsViewSet)
router.register('tags', GetTagsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('users/', UserSignUpAndView.as_view()),
    path('users/<int:pk>/', UserProfiles.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/', UserProfile.as_view()),
    path('users/set_password/', UserSetPassword.as_view()),
    path('users/subscriptions/', UserSubscriptions.as_view()),
    path('users/<int:pk>/subscribe/', AddSubView.as_view()),
    path('', include(router.urls)),
]
