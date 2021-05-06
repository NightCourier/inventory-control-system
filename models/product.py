from django.db import models

from .category import Category
from .storage import Storage


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    bar_code = models.BigIntegerField(verbose_name="Штрих-код")
    vendor_code = models.CharField(max_length=255, verbose_name="Артикул")
    amount = models.IntegerField(verbose_name="Количество")
    price = models.FloatField(verbose_name="Цена")
    description = models.CharField(max_length=255, verbose_name="Описание")
    details = models.CharField(max_length=255, verbose_name="Характеристика товара")
    storage = models.ManyToManyField(Storage, verbose_name="Склад")
    product_type = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products"
    )

    @property
    def total_price(self):
        return self.amount * self.price

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
