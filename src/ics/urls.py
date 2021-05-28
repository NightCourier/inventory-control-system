from django.urls import path
from ics.views import ProductListView, update_product, ProductDeleteView

urlpatterns = [
    path(r'<slug:slug>/<str:name>', ProductListView.as_view(), name="home"),  # item_by_category
    path('update/<int:pk>/<str:product_type>/<slug:slug>', update_product, name="edit"),
    path('<slug:slug>/<str:product_type>/<int:pk>', ProductDeleteView.as_view(), name="delete")
]
