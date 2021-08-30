from django.urls import path
from auth_app import views

urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('user/<int:id>/', views.UserView.as_view())
]