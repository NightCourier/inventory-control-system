import json

import xlsxwriter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView, UpdateView

from .queries import *
from .validation import get_booked_amount


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
        if product.amount_available:
            amount_booked = get_booked_amount(request, product)
            product.amount_available -= amount_booked
            product.save()
            insert_data_to_order_table(user_id=request.user.id, product_id=self.kwargs["pk"],
                                       amount=amount_booked)
            return super().post(request, **kwargs)
        return super().post(request, **kwargs)


class ExcelWriter:
    @staticmethod
    def _get_map_data(user_id):
        order_data = get_order_data_by_user(user_id)
        mapped_data = defaultdict(int)

        for item in order_data:
            mapped_data[item.product.id] += item.amount

        return mapped_data

    @staticmethod
    def _get_map_id_price(user_id):
        id_price = defaultdict(float)
        for product_id, amount in ExcelWriter._get_map_data(user_id).items():
            id_price[product_id] = get_product_price(product_id) * amount

        return id_price

    @staticmethod
    def _get_product_id_name(user_id):
        mapped = defaultdict(str)

        for item in get_order_data_by_user(user_id):
            mapped[item.product.id] = get_product_name(item.product.id)

        return mapped

    @staticmethod
    def _get_total(user_id):
        return sum([v for k, v in ExcelWriter._get_map_id_price(user_id).items()])

    @staticmethod
    def populate_data_to_excel(response, user_id):
        with xlsxwriter.Workbook(response, {'in_memory': True}) as workbook:
            worksheet = workbook.add_worksheet()
            total = ExcelWriter._get_total(user_id)
            price = ExcelWriter._get_map_id_price(user_id)
            name = ExcelWriter._get_product_id_name(user_id)
            amount = ExcelWriter._get_map_data(user_id)

            header_format = workbook.add_format()
            header_format.set_bold()
            header_format.set_bg_color("green")
            header_format.set_font_size(15)

            data_format = workbook.add_format()
            data_format.set_font_size(13)

            row = 5

            worksheet.write('A1',
                            f'Забронированный товар пользователем {get_first_name(user_id)} {get_last_name(user_id)}',
                            header_format)
            worksheet.write('A4', 'Наименование товара', header_format)
            worksheet.write('B4', f'Количество забронированного', header_format)
            worksheet.write('C4', f'Сумма', header_format)

            for key, value in name.items():
                worksheet.write(f'A{row}', f'{value}', data_format)
                worksheet.write(f'B{row}', f'{amount[key]}', data_format)
                worksheet.write(f'C{row}', f'{price[key]}', data_format)
                row += 1

            worksheet.write(f'A{row + 1}', 'Общая сумма забронированного товара', header_format)
            worksheet.write(f'B{row + 1}', '', header_format)
            worksheet.write(f'C{row + 1}', f'{total}', header_format)


def report(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="report.xlsx"'

    ExcelWriter.populate_data_to_excel(response, user_id=request.user.id)
    return response
