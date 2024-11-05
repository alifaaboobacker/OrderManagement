from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('signup',RegistrationView.as_view(),name="register"),
]