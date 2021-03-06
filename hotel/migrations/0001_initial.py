# Generated by Django 4.0.1 on 2022-02-27 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя оборудования')),
                ('wearout', models.IntegerField(default=0, verbose_name='Износ')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя типа оборудования')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('pasprot_series', models.CharField(max_length=10, verbose_name='Серия паспорта')),
                ('pasprot_number', models.CharField(max_length=10, verbose_name='Номер паспорта')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя категориии')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mumber', models.IntegerField(unique=True, verbose_name='Номер')),
                ('status', models.CharField(max_length=15, verbose_name='Статус')),
                ('rooms_qty', models.IntegerField(verbose_name='Кол-во комнат')),
                ('sleeper_qty', models.IntegerField(verbose_name='Кол-во спальных мест')),
                ('daily_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Цена в сутки')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomtype', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='Количество')),
                ('enquipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.equipment', verbose_name='Оборудование')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room', verbose_name='Номер')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.equipmenttype', verbose_name='Тип оборудования'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('deposit', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Депозит')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Цена всего')),
                ('status', models.CharField(max_length=15, verbose_name='Статус')),
                ('guests', models.ManyToManyField(blank=True, related_name='related_booking', to='hotel.Guest')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room', verbose_name='Номер')),
            ],
        ),
    ]
