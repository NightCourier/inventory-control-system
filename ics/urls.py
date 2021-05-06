from django.urls import path
from ics.views import ProductListView

urlpatterns = [
    path('<slug:slug>', ProductListView.as_view(), name="home"),  # item_by_category
]
