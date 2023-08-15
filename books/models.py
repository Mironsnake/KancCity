
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    title  = models.CharField(max_length = 200, verbose_name='Название')
    author = models.CharField(max_length = 200, verbose_name='Автор')
    description = models.CharField(max_length = 500, default=None, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    image_url = models.CharField(max_length = 2083, default=False)
    year_published = models.PositiveIntegerField(null=True, blank=True, verbose_name='Год издания')  # Заменили поле follow_author на year_published  
    book_available = models.BooleanField(default=True, verbose_name='В наличии')
    category = models.CharField(max_length=100, blank=True, verbose_name='Категория')
    content = models.TextField(blank=True, verbose_name='Текст книги')  # Новое поле для текста книги
    PURCHASE = 'PURCHASE'
    RENT_1_MONTH = 'RENT_1_MONTH'
    RENT_3_MONTHS = 'RENT_3_MONTHS'
    OPERATION_CHOICES = [
        (PURCHASE, 'Покупка'),
        (RENT_1_MONTH, 'Аренда на 1 месяц'),
        (RENT_3_MONTHS, 'Аренда на 3 месяца'),
    ]
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, default=PURCHASE)
    rent_price = models.FloatField(null=True, blank=True, verbose_name='Стоимость аренды')

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=20)  # Без default


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
   

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

