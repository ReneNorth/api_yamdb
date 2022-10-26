from django.urls import path
from .views import SignupView, ObtainUserTokenView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('token/', ObtainUserTokenView.as_view()),
    path('signup/', SignupView.as_view(), name='auth_register'),
]