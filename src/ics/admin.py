from django.contrib import admin

from .models import Product, Category, Storage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Storage)
admin.site.site_url = '/products/admin/Техника'
