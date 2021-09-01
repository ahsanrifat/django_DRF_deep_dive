from django.urls import path
from auth_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("user/", views.UserView.as_view()),
    path("user/<int:id>/", views.UserView.as_view()),
    path("user/auth/", views.LoginView.as_view()),
    path("user/logout/", views.LogoutView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/list/view", views.ListViewExample.as_view()),
]
