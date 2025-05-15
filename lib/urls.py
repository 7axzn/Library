from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('search/', views.search_books, name='search_books'),
    path('view/', views.userShow_book, name='view_books'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    

    # Admin paths
    path('admin/add/', views.add_book, name='add_book'),
    path('admin/view/', views.adminShow_book, name='admin_showbook'),
    path('admin/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('admin/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
