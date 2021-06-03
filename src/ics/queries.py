from collections import defaultdict

from django.utils import timezone

from .models import Product, Storage, Category, Order, User


def get_category_id_by_name(name):
    return Category.objects.filter(name=name).first().id


def get_category_name(name):
    return Category.objects.filter(name=name).first().name


def get_city(slug):
    return Storage.objects.filter(slug=slug).first().city


def get_total_by_category(name, slug):
    return round(
        sum([item.total for item in get_products_by_category(name, slug)]), 2)


def get_products_by_category(name, slug):
    return Product.objects.filter(storage__slug=slug, product_type_id=get_category_id_by_name(name))


def get_products_by_slug(slug):
    return Product.objects.filter(storage__slug=slug)


def get_total_by_slug(slug):
    return sum([item.total for item in get_products_by_slug(slug)])


def get_category_price(slug):
    category_total = defaultdict()
    categories = Category.objects.all()

    for category in categories:
        category_total[category.name] = round(
            sum([item.total for item in Product.objects.filter(
                product_type=category.id, storage__slug=slug)]), 2)
    return category_total


def get_first_category_name():
    return Category.objects.all().first()


def insert_data_to_order_table(user_id, product_id, amount):
    Order.objects.create(user=_get_user_id(user_id), product=_get_product_id(product_id), amount=amount,
                         order_time=timezone.now())


def _get_user_id(request_id):
    return User.objects.filter(id=request_id).first().id


def _get_product_id(request_product_id):
    return Product.objects.filter(id=request_product_id).first()


def get_first_name(user_id):
    return User.objects.filter(id=user_id).first().first_name


def get_last_name(user_id):
    return User.objects.filter(id=user_id).first().last_name


def get_order_data_by_user(user_id):
    return Order.objects.filter(user=user_id).all()


def get_product_name(pk):
    return Product.objects.filter(id=pk).first().name


def get_product_price(pk):
    return Product.objects.filter(id=pk).first().price
