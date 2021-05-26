import json
from collections import defaultdict

from django.views.generic import ListView

from .models import Product, Storage, Category


class ProductListView(ListView):
    template_name = "ics/table.html"
    context_object_name = 'storproducts'

    def get_queryset(self):
        category_total = defaultdict()
        categories = Category.objects.all()

        for category in categories:
            category_total[category.name] = round(
                sum([item.total for item in Product.objects.filter(
                    product_type=category.id, storage__slug=self.kwargs['slug'])]), 2)
        content = {
            'products': Product.objects.filter(storage__slug=self.kwargs['slug']),
            'category_price': category_total
        }
        return content

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['total'] = json.dumps(context['object_list']['category_price'])
        context['storages'] = Storage.objects.all()
        context['storage_price'] = round(Storage.objects.filter(slug=self.kwargs['slug']).first().total_price, 2)
        context['city'] = Storage.objects.filter(slug=self.kwargs['slug']).first().city
        return context
