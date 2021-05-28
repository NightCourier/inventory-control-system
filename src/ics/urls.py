from django.urls import path
from ics.views import ProductListView

urlpatterns = [
    path('<slug:slug>/<str:name>', ProductListView.as_view(), name="home")
]
