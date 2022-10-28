from django.urls import path

from .views import ObtainUserTokenView, SignupView

urlpatterns = [
    path('token/', ObtainUserTokenView.as_view()),
    path('signup/', SignupView.as_view(), name='auth_register'),
]
