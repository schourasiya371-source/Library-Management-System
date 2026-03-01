"""
URL patterns for the library app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Home & Auth ────────────────────────────────────────────
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.student_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    # ── Admin ──────────────────────────────────────────────────
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Books
    path('books/add/', views.add_book, name='add_book'),
    path('books/', views.view_books, name='view_books'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Categories
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # Students
    path('students/', views.view_students, name='view_students'),

    # Issue Management (Admin)
    path('issue-book/', views.issue_book_admin, name='issue_book_admin'),
    path('issued-books/', views.view_issued_books, name='view_issued_books'),
    path('return-book/<int:pk>/', views.return_book_admin, name='return_book_admin'),

    # ── Student ────────────────────────────────────────────────
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('search/', views.search_books, name='search_books'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('request-issue/<int:pk>/', views.request_issue, name='request_issue'),
    path('my-books/', views.my_books, name='my_books'),
    path('history/', views.issue_history, name='issue_history'),
]
