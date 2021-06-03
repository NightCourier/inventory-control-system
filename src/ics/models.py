from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Storage(models.Model):
    city = models.CharField(max_length=255, verbose_name="Город")
    group = models.CharField(max_length=255, verbose_name="Группа")
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    @property
    def total_price(self):
        return sum([product.total for product in self.product_set.all()])

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
    amount_available = models.IntegerField(verbose_name="Количество доступных")
    amount_booked = models.IntegerField(verbose_name="Количество забронированных", default=0)
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
    def total(self):
        return self.amount_available * self.price

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home', args=[str(self.storage.first().slug), str(self.product_type)])

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Order(models.Model):
    user = models.IntegerField()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт"
    )

    amount = models.IntegerField()
    order_time = models.DateTimeField()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
