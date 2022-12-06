from django.urls import include, path
from recipes.views import GetIngredientsViewSet, GetTagsViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('ingredients', GetIngredientsViewSet)
router.register('tags', GetTagsViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('', include(router.urls)),
]
