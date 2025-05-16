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




def index(request):
    return render(request, 'index.html')

# authentication

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        user_type = request.POST.get("user-type")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")
        

        

        User.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        messages.success(request, "Account created successfully.")
        return redirect("login")  

    return render(request, "signup.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.user_type == 'admin':
             return redirect('admin_dashboard') 
            else:
                return redirect('user_dashboard') 
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")


# USER VIEWS

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def userShow_book(request):  # View books
    books = Book_Details.objects.all()
    return render(request, 'user_view_books.html', {'books': books})

def search_books(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Book_Details.objects.filter(
            Q(Name__icontains=query) | Q(Author__icontains=query)
        )

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

from django.contrib.auth import get_user_model
User = get_user_model()

def borrow_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book_Details, id=book_id)

        if book.Availability.lower() == 'available':
            book.Availability = 'Borrowed'
            book.save()

            user = request.user
            user.borrowed_books.add(book)  
            user.save()

            messages.success(request, f"Successfully borrowed {book.Name}")
            return redirect('borrowed_books')

        else:
            messages.error(request, "This book is not available for borrowing")
            return redirect('book_details', book_id=book_id)

    return redirect('user_view_book')

# ADMIN VIEWS

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
                return redirect('add_book')
            except ValueError:
                return render(request, 'admin_add_book.html', {
                    'error': 'Invalid date format. Please use YYYY-MM-DD.'
                })
        else:
            return render(request, 'admin_add_book.html', {
                'error': 'Please fill in all the required fields.'
            })

    return render(request, 'admin_add_book.html')


def adminShow_book(request):
    books = Book_Details.objects.all()
    return render(request, 'admin_view_books.html', {'books': books})


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

        return redirect('admin_showbook')

    return render(request, 'admin_edit_book.html', {'book': book})


def delete_book(request, book_id):
    book = get_object_or_404(Book_Details, id=book_id)
    book.delete()
    return redirect('admin_showbook')



def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

