from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('vendor_code', 'name', 'bar_code', 'amount', 'price')
