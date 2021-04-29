from django.db import models


class Storage(models.Model):
    city = models.CharField(max_length=255, verbose_name="Город")
    group = models.CharField(max_length=255, verbose_name="Группа")
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товара"


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
