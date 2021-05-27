import json

from django.views.generic import ListView

from .queries import *


class ProductListView(ListView):
    template_name = "ics/table.html"
    context_object_name = 'storproducts'

    def get_queryset(self):
        if self.kwargs['name'] == 'all':
            content = {
                'products': get_products_by_slug(self.kwargs['slug']),
                'total': get_total_by_slug(self.kwargs['slug']),
                'city': get_city(self.kwargs['slug']),
                'category_price': get_category_price(self.kwargs['slug']),
                'slug': self.kwargs['slug'],
                'category': get_first_category_name(),
                'isAllStorage': True
            }
            return content

        content = {
            'products': get_products_by_category(self.kwargs['name'], self.kwargs['slug']),
            'city': get_city(self.kwargs['slug']),
            'category_price': get_total_by_category(self.kwargs['name'], self.kwargs['slug']),
            'slug': self.kwargs['slug'],
            'category': get_category_name(self.kwargs['name']),
            'isAllStorage': False,
        }

        return content

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['isAllStorage'] = json.dumps(context['object_list']['isAllStorage'])
        context['total'] = json.dumps(context['object_list']['category_price'])
        context['categories'] = Category.objects.all()
        context['storages'] = Storage.objects.all()
        context['storage_price'] = round(Storage.objects.filter(slug=self.kwargs['slug']).first().total_price, 2)
        context['city'] = Storage.objects.filter(slug=self.kwargs['slug']).first().city
        return context
