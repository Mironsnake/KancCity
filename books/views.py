from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order, UserBook
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from .tasks import send_rent_reminder




class BooksListView(ListView):
    model = Book
    template_name = 'list.html'
    ordering = '-id'  # По умолчанию сортируем по id (можно поменять на другое поле)

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort-by')

        # Применяем сортировку в соответствии с выбранным параметром
        if sort_by == 'author':
            queryset = queryset.order_by('author')
        elif sort_by == 'year_published':
            queryset = queryset.order_by('year_published')
        elif sort_by == 'category':
            queryset = queryset.order_by('category')

        return queryset


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
    context_object_name = 'book'  # Указываем имя переменной для объекта книги

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Здесь можно добавить логику для получения и передачи других данных в контекст
        return context

class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        # Фильтруем поисковый запрос
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )

        # Получаем выбранный параметр сортировки
        sort_by = self.request.GET.get('sort-by')

        # Применяем сортировку в соответствии с выбранным параметром
        if sort_by == 'author':
            queryset = queryset.order_by('author')
        elif sort_by == 'year_published':
            queryset = queryset.order_by('year_published')
        elif sort_by == 'category':
            queryset = queryset.order_by('category')

        return queryset

class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'login'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Book.objects.get(id=body['productId'])
	Order.objects.create(
		product=product
	)
	return JsonResponse('Payment completed!', safe=False)


@login_required  # Добавляем декоратор, чтобы представление было доступно только администратору
def create_book(request):
    if request.method == 'POST':
        # Получаем данные из POST запроса
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        year_published = request.POST.get('year_published')
        category = request.POST.get('category')
        book_available = request.POST.get('book_available')

        # Создаем новую книгу
        Book.objects.create(
            title=title,
            author=author,
            description=description,
            price=price,
            image_url=image_url,
            year_published=year_published,
            category=category,
            book_available=book_available,
        )

        # Перенаправляем пользователя на страницу со списком книг
        return redirect('list')

    return render(request, 'create_book.html')



@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_orders': user_orders})

def book_text_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_text.html', {'book': book})

    
def render_modal_response(request, template_name, context):
    html = render_to_string(template_name, context, request=request)
    return JsonResponse({'html': html})


def modal_success_view(request):
    return render(request, 'modal_success.html')

@login_required
def purchase_rent_book(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        operation = request.POST.get('operation')

        if operation in ['PURCHASE', 'RENT_1_MONTH', 'RENT_3_MONTHS']:
            user_orders = Order.objects.filter(user=request.user, product=book, operation=operation)
            if not user_orders:
                order = Order.objects.create(user=request.user, product=book, operation=operation)

                # Вызываем задачу на отправку уведомления о завершении срока аренды
                send_rent_reminder(order.id)

                return redirect('profile')
            else:
                message = "Вы уже совершили данную операцию с этой книгой."
    return JsonResponse({'error': 'Invalid request method or operation.'}, status=400)
