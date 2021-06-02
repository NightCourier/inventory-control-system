from django.urls import path
from ics.views import ProductListView, ProductUpdateView, ProductDeleteView, ProductBookView

urlpatterns = [
    path(r'<slug:slug>/<str:name>', ProductListView.as_view(), name="home"),
    path('update/<int:pk>/<str:product_type>/<slug:slug>', ProductUpdateView.as_view(), name="edit"),
    path('delete/<slug:slug>/<str:product_type>/<int:pk>', ProductDeleteView.as_view(), name="delete"),
    path('book/<slug:slug>/<str:product_type>/<int:pk>', ProductBookView.as_view(), name="book")
]
