from django.views.generic import ListView
from .models import Product, Storage


class ProductListView(ListView):
    template_name = "ics/table.html"
    context_object_name = 'catproduct'

    def get_queryset(self):
        content = {
            'city': Storage.objects.filter(slug=self.kwargs['slug']).first().city,
            'products': Product.objects.filter(storage__slug=self.kwargs['slug'])
        }
        return content

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['storages'] = Storage.objects.all()
        return context
