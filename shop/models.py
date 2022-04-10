from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .manager import CustomUserManager


class Customer(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    contact = models.CharField(max_length=255, verbose_name='Контакты')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Manufacturer(models.Model):  # Производитель
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя производителя')
    content = models.TextField(blank=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='photos/manufacturer/%Y/%m/%d', verbose_name='Лого')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя категории')
    content = models.TextField(blank=True, verbose_name='Описание')
    is_availability = models.BooleanField(default=False, verbose_name='Доступность')
    quantity = models.IntegerField(default=0, verbose_name='Кол-во в наличии')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя товара')
    content = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='photos/product/%Y/%m/%d', verbose_name='Изображение')
    model = models.CharField(max_length=255, blank=False, verbose_name='Модель товара')
    price = models.FloatField(verbose_name='Цена')
    is_availability = models.BooleanField(default=False, verbose_name='Доступность')
    quantity = models.IntegerField(default=0, verbose_name='Кол-во в наличии')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    manuf = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, verbose_name='Производитель')

    def get_order_url(self):
        return reverse('order', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Status(models.Model):
    title = models.CharField(max_length=255, verbose_name='Этап доставки')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.title


class DeliveryMethod(models.Model):
    delivery_name = models.CharField(max_length=255, verbose_name='Транспортная компания')

    class Meta:
        verbose_name = 'Транспортная компания'
        verbose_name_plural = 'Транспортная компании'

    def __str__(self):
        return self.delivery_name


class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=255, verbose_name='Платёжная система')

    def __str__(self):
        return self.payment_method

    class Meta:
        verbose_name = 'Платёжная система'
        verbose_name_plural = 'Платёжная системы'


class Order(models.Model):
    all_price = models.FloatField(verbose_name='Цена всего заказа')
    comment = models.TextField(blank=True, verbose_name='Описание')
    amount = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, verbose_name='Товар')
    delivery_status = models.ForeignKey('Status', on_delete=models.DO_NOTHING, verbose_name='Статус доставки')
    delivery_name = models.ForeignKey('DeliveryMethod', on_delete=models.DO_NOTHING, verbose_name='Способ доставки')
    # Домой курьером, пункт выдачи, почта, транспортной компанией
    payment = models.ForeignKey('PaymentMethod', on_delete=models.DO_NOTHING, verbose_name='Способ оплаты')

    def __str__(self):
        return self.pk + "." + self.customer

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
