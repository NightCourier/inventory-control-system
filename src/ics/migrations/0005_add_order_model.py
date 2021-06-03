import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ics', '0004_auto_20210602_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    verbose_name="Продукт",
                    to="ics.product"
                )),
                ('amount', models.IntegerField()),
                ('order_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
