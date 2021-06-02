import json
from django.views.generic import ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .queries import *


class ProductListView(PermissionRequiredMixin, ListView):
    permission_required = 'ics.view_product'
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


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = 'ics.change_product'

    model = Product
    fields = ['vendor_code', 'name', 'bar_code', 'amount_available', 'price']
    template_name_suffix = '_update_form'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = 'ics.delete_product'

    model = Product

    def get_success_url(self):
        return f'/products/{self.kwargs["slug"]}/{self.kwargs["product_type"]}'


class ProductBookView(UpdateView):
    raise_exception = True
    permission_required = 'ics.view_product'

    model = Product
    fields = ["amount_booked"]
    template_name_suffix = '_book'

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["pk"])
        product.amount_available -= int(request.POST["amount_booked"]) if product.amount_booked != int(request.POST["amount_booked"]) else 0
        product.save()
        return super().post(request, **kwargs)
