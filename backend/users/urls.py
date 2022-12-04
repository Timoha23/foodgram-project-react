from django.urls import path
from .views import (UserSignUpAndView, UserProfileView,
                    MeUserProfileView, UserSetPasswordView,
                    UserFollowView, AddFollowView)


urlpatterns = [
    path('', UserSignUpAndView.as_view()),
    path('<int:pk>/', UserProfileView.as_view()),
    path('me/', MeUserProfileView.as_view()),
    path('set_password/', UserSetPasswordView.as_view()),
    path('subscriptions/', UserFollowView.as_view()),
    path('<int:pk>/subscribe/', AddFollowView.as_view()),
]
