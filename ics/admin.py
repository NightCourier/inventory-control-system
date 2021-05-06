from django.contrib import admin
from models.product import Product
from models.storage import Storage
from models.category import Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Storage)
