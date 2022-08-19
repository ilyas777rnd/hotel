from django.db import models
from django.contrib.auth.models import User


# Табл.1 Тип Оборудования
class EquipmentType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя типа оборудования')

    def __str__(self):
        return self.name


# Табл.2 Тип Номера
class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя категориии')

    def __str__(self):
        return self.name


# Табл.3 Гость
class Guest(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    pasprot_series = models.CharField(max_length=10, verbose_name='Серия паспорта')
    pasprot_number = models.CharField(max_length=10, verbose_name='Номер паспорта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.CharField(max_length=100, verbose_name='Email')
    birth_date = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.name} {self.surname} {self.pasprot_series} {self.pasprot_number}'


# Табл.4 Оборудование
class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя оборудования')
    type = models.ForeignKey(EquipmentType, verbose_name='Тип оборудования', on_delete=models.CASCADE)
    wearout = models.IntegerField(default=0, verbose_name='Износ')

    def __str__(self):
        return f'{self.name} {self.type.name}'


# Табл.5 Комната
class Room(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер')
    status = models.CharField(max_length=15, verbose_name='Статус')
    rooms_qty = models.IntegerField(verbose_name='Кол-во комнат')
    sleeper_qty = models.IntegerField(verbose_name='Кол-во спальных мест')
    daily_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Цена в сутки')
    type = models.ForeignKey(RoomType, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number} {self.type.name}'


# Табл.6 Бронирование
class Booking(models.Model):
    room = models.ForeignKey(Room, verbose_name='Номер', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    deposit = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Депозит')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Цена всего')
    status = models.CharField(max_length=15, verbose_name='Статус')
    manager = models.ForeignKey(User, verbose_name='Менеджер', null=True, on_delete=models.CASCADE)
    guests = models.ManyToManyField(Guest, blank=True, related_name='related_booking')

    def __str__(self):
        return f'Комната {self.room.number}, c {self.start_date} по {self.end_date}, всего {self.total} У.Е.'


# Табл.7 Список оборудования
class EquipmentList(models.Model):
    enquipment = models.ForeignKey(Equipment, verbose_name='Оборудование', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name='Номер', on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.enquipment.name}, комната {self.room.number} - {self.qty} шт.'
