"""
Models for the College Library Management System.

Models:
    - Category: Book categories (e.g., Science, Fiction)
    - Book: Individual book records with images, quantity, availability
    - StudentProfile: Extends Django User for student-specific data
    - IssuedBook: Tracks book issues, returns, fines, and due dates
"""

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    """Book categories for organizing the library collection."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Represents a book in the library."""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='books'
    )
    description = models.TextField(blank=True, default='')
    cover_image = models.ImageField(
        upload_to='book_covers/', blank=True, null=True
    )
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    publisher = models.CharField(max_length=200, blank=True, default='')
    edition = models.CharField(max_length=50, blank=True, default='')
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        """Check if the book has copies available for issue."""
        return self.available_quantity > 0


class StudentProfile(models.Model):
    """Extended profile for student users."""
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        ('IT', 'Information Technology'),
        ('OTHER', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    enrollment_no = models.CharField('Enrollment Number', max_length=30, unique=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, default='CSE')
    phone = models.CharField(max_length=15, blank=True, default='')
    profile_pic = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_no})"


class IssuedBook(models.Model):
    """Records for book issues, tracking due dates and fines."""
    STATUS_CHOICES = [
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ISSUED')
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.title} → {self.student.get_full_name()}"

    def save(self, *args, **kwargs):
        # Auto-set due date if not provided
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(
                days=settings.ISSUE_DURATION_DAYS
            )
        super().save(*args, **kwargs)

    @property
    def calculated_fine(self):
        """Calculate fine based on overdue days."""
        if self.status == 'RETURNED' and self.return_date:
            end = self.return_date
        else:
            end = timezone.now()
        if end > self.due_date:
            overdue_days = (end - self.due_date).days
            return overdue_days * settings.FINE_PER_DAY
        return 0

    @property
    def is_overdue(self):
        """Check if the book is past due date and not yet returned."""
        if self.status == 'RETURNED':
            return False
        return timezone.now() > self.due_date

    @property
    def days_remaining(self):
        """Days remaining until due date (negative if overdue)."""
        if self.status == 'RETURNED':
            return 0
        delta = self.due_date - timezone.now()
        return delta.days
