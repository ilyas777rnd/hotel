# Generated by Django 3.2.13 on 2022-05-07 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_delete_salesorder'),
        ('products', '0002_product_image_product_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
