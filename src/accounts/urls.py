from django.urls import path, include
from .views import WelcomePageView

urlpatterns = [
    path('welcome/', WelcomePageView.as_view(), name="welcome"),
    path('', include("django.contrib.auth.urls")),
]