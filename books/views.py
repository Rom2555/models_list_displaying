from datetime import date

from django.utils import timezone
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('-pub_date')

    context = {'books': books}
    return render(request, template, context)


def books_by_date(request, pub_date):
    template = 'books/books_by_date.html'

    # Преобразуем строку в объект date
    try:
        target_date = date.fromisoformat(pub_date)
    except ValueError:
        raise Http404("Некорректный формат даты. Требуется формат YYYY-MM-DD.")

    # Получаем книги за указанную дату
    books = Book.objects.filter(pub_date=target_date).order_by('-pub_date')

    if not books.exists():
        raise Http404("Книг на указанную дату не найдено")


    # Получаем уникальные даты публикаций для навигации
    all_dates = sorted(set(Book.objects.values_list('pub_date', flat=True)))
    all_dates_str = [d.isoformat() for d in all_dates]

    try:
        current_index = all_dates_str.index(pub_date)
        prev_date = all_dates_str[current_index - 1] if current_index > 0 else None
        next_date = all_dates_str[current_index + 1] if current_index < len(all_dates_str) - 1 else None
    except ValueError:
        raise Http404("Указанная дата отсутствует в базе данных")

    context = {
        'books': books,
        'current_date': pub_date,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, template, context)


def test_home(request):
    return HttpResponse(f"""
    <h1>✅ НОВЫЙ ПРОЕКТ models_list_displaying</h1>
    <p>Время запуска: {timezone.now()}</p>
    <p>Папка: C:\\Users\\furer\\Desktop\\models_list_displaying</p>
    """)