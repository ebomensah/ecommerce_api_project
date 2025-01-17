from django.urls import path
from .views import RegisterView, LoginView, LogOutView


urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogOutView.as_view(), name='logout'),
]