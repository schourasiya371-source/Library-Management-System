"""
Django Admin registration for library models.
"""
from django.contrib import admin
from .models import Category, Book, StudentProfile, IssuedBook


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'total_quantity', 'available_quantity')
    list_filter = ('category',)
    search_fields = ('title', 'author', 'isbn')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_no', 'branch', 'phone')
    search_fields = ('user__username', 'enrollment_no')


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issue_date', 'due_date', 'status', 'fine')
    list_filter = ('status',)
    search_fields = ('book__title', 'student__username')
