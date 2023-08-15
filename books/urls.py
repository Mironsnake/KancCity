from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksListView.as_view(), name='list'),
    path('<int:pk>/', views.BooksDetailView.as_view(), name='detail'),
    path('<int:pk>/checkout/', views.BookCheckoutView.as_view(), name='checkout'),
    path('complete/', views.paymentComplete, name='complete'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    path('create_book/', views.create_book, name='create_book'),
    path('book/<int:pk>/purchase_rent/', views.purchase_rent_book, name='purchase_rent_book'),
    path('profile/', views.profile, name='profile'),
    path('book/<int:book_id>/text/', views.book_text_view, name='book_text'),
    path('modal_success/', views.modal_success_view, name='modal_success'),
]
