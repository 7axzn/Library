from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
from lib.models import Book_Details
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.contrib.auth import authenticate, login ,logout
from .models import CustomUser
from django.contrib.auth import get_user_model

from django.http import JsonResponse

from django.db.models import Q




def index(request):
    return render(request, 'index.html')

# authentication

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('admin_dashboard' if user.user_type == 'admin' else 'user_dashboard')})
            return redirect('admin_dashboard' if user.user_type == 'admin' else 'user_dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        user_type = request.POST.get("user-type")
        if password != confirm_password:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Passwords do not match.'})
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")
        if User.objects.filter(username=username).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Username already taken.'})
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")
        User.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': reverse('login')})
        messages.success(request, "Account created successfully.")
        return redirect("login")
    return render(request, "signup.html")


# USER VIEWS

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def userShow_book(request):  # View books
    books = Book_Details.objects.all()
    return render(request, 'user_view_books.html', {'books': books})


def search_books(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = Book_Details.objects.filter(
            Q(Name__icontains=query) |
            Q(Author__icontains=query) |
            Q(Category__icontains=query) |
            Q(Description__icontains=query) |
            Q(Availability__icontains=query)
        )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(results.values('id', 'Name', 'Author', 'Category', 'Availability'))
        return JsonResponse({'results': data})
    return render(request, 'user_search_books.html', {
        'query': query,
        'results': results,
    })

def book_details(request, book_id):
    book = get_object_or_404(Book_Details, id=book_id)
    return render(request, 'user_book_details.html', {'book': book})

def borrowed_books(request):
    books = request.user.borrowed_books.all() if request.user.is_authenticated else []
    return render(request, 'user_borrowed_books.html', {'borrowed_books': books})

User = get_user_model()

def borrow_book(request, book_id):
    book = get_object_or_404(Book_Details, id=book_id)
    if request.method == "POST":
        if book.Availability.lower() == 'available':
            book.Availability = 'Borrowed'
            book.save()
            user = request.user
            user.borrowed_books.add(book)
            user.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Successfully borrowed {book.Name}'})
            messages.success(request, f"Successfully borrowed {book.Name}")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'This book is not available for borrowing'})
            messages.error(request, "This book is not available for borrowing")
    return redirect('borrowed_books')

def return_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book_Details, id=book_id)
        if book in request.user.borrowed_books.all():
            book.Availability = 'Available'
            book.save()
            user = request.user
            user.borrowed_books.remove(book)
            user.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Successfully returned {book.Name}'})
            messages.success(request, f"Successfully returned {book.Name}")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'You have not borrowed this book'})
            messages.error(request, "You have not borrowed this book")
    return redirect('borrowed_books')

# ADMIN VIEWS

def adminShow_book(request):
    books = Book_Details.objects.all()
    return render(request, 'admin_view_books.html', {'books': books})

def add_book(request):
    if request.method == "POST":
        name = request.POST.get('Name', '')
        author = request.POST.get('Author', '')
        category = request.POST.get('Category', '')
        description = request.POST.get('Description', '')
        date = request.POST.get('Date_Added', '')
        availability = request.POST.get('Availability', '')
        if name and author and category and description and date and availability:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                Book_Details.objects.create(
                    Name=name,
                    Author=author,
                    Category=category,
                    Description=description,
                    Date_Added=date_obj,
                    Availability=availability
                )
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Book added successfully'})
                return redirect('add_book')
            except ValueError:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Invalid date format'})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please fill in all the required fields.'})
    return render(request, 'admin_add_book.html')

def edit_book(request, book_id):
    book = get_object_or_404(Book_Details, id=book_id)
    if request.method == "POST":
        book.Name = request.POST.get('Name')
        book.Author = request.POST.get('Author')
        book.Category = request.POST.get('Category')
        book.Description = request.POST.get('Description')
        date_added = request.POST.get('Date_Added')
        book.Availability = request.POST.get('Availability')
        book.Date_Added = datetime.strptime(date_added, '%Y-%m-%d').date()
        book.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Book updated successfully'})
        return redirect('admin_showbook')
    return render(request, 'admin_edit_book.html', {'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book_Details, id=book_id)
    if request.method == "POST":
        book.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Book deleted successfully'})
    return redirect('admin_showbook')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

