from django.contrib import admin
from .models import Book, Order

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'book_available', 'category', 'operation', 'rent_price']
    list_filter = ['book_available', 'category', 'operation']
    search_fields = ['title', 'author', 'category']

admin.site.register(Book, BookAdmin)
admin.site.register(Order)
