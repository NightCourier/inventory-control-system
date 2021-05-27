from collections import defaultdict

from .models import Product, Storage, Category


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