from django.db.models import Sum
from django.views.generic import ListView

from models.category import Category
from models.product import Product
from models.storage import Storage


class ProductListView(ListView):
    template_name = "ics/table.html"
    context_object_name = 'storproducts'

    def get_queryset(self):
        content = {
            'city': Storage.objects.filter(slug=self.kwargs['slug']).first().city,
            'products': Product.objects.filter(storage__slug=self.kwargs['slug']),
            'price': Category.objects.annotate(total_price=Sum('products__price'))
        }
        return content

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['storages'] = Storage.objects.all()
        return context
