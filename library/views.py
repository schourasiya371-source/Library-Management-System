"""
Views for the College Library Management System.

Sections:
    1. Authentication views (login, signup, logout)
    2. Home / landing page
    3. Admin views (dashboard, book CRUD, student management, issue management)
    4. Student views (dashboard, search, issue request, history)
"""

from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from .models import Book, Category, IssuedBook, StudentProfile
from .forms import StudentSignupForm, BookForm, IssueBookForm, CategoryForm
from .decorators import admin_required, student_required


# ═══════════════════════════════════════════════════════════════
#  HOME & AUTHENTICATION
# ═══════════════════════════════════════════════════════════════

def home(request):
    """Landing page — redirect authenticated users to their dashboard."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
    return render(request, 'library/home.html')


def user_login(request):
    """Unified login view for students and admins."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'library/login.html')


def student_signup(request):
    """Registration view for new students."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Registration successful! Please log in.'
            )
            # Send welcome email
            try:
                send_mail(
                    subject='Welcome to College Library',
                    message=(
                        f'Hi {user.first_name},\n\n'
                        'Your account has been created successfully.\n'
                        'You can now log in and start exploring books!\n\n'
                        'Happy Reading!\nCollege Library Team'
                    ),
                    from_email='library@college.edu',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                pass  # Email is optional; don't block signup
            return redirect('login')
    else:
        form = StudentSignupForm()
    return render(request, 'library/signup.html', {'form': form})


def user_logout(request):
    """Log the user out and redirect to login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ═══════════════════════════════════════════════════════════════
#  ADMIN VIEWS
# ═══════════════════════════════════════════════════════════════

@admin_required
def admin_dashboard(request):
    """Admin dashboard with key statistics."""
    total_books = Book.objects.count()
    total_copies = Book.objects.aggregate(total=Sum('total_quantity'))['total'] or 0
    total_students = StudentProfile.objects.count()
    issued_books = IssuedBook.objects.filter(status='ISSUED').count()
    overdue_books = IssuedBook.objects.filter(
        status='ISSUED', due_date__lt=timezone.now()
    ).count()
    returned_books = IssuedBook.objects.filter(status='RETURNED').count()
    total_fines = IssuedBook.objects.aggregate(total=Sum('fine'))['total'] or 0
    recent_issues = IssuedBook.objects.select_related('book', 'student')[:5]
    categories = Category.objects.count()

    context = {
        'total_books': total_books,
        'total_copies': total_copies,
        'total_students': total_students,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'returned_books': returned_books,
        'total_fines': total_fines,
        'recent_issues': recent_issues,
        'categories': categories,
    }
    return render(request, 'library/admin_dashboard.html', context)


# ── Book CRUD ──────────────────────────────────────────────────

@admin_required
def add_book(request):
    """Add a new book to the library."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.available_quantity = book.total_quantity
            book.save()
            messages.success(request, f'"{book.title}" added successfully!')
            return redirect('view_books')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


@admin_required
def view_books(request):
    """List all books with search and filter."""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    books = Book.objects.select_related('category')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all()
    context = {
        'books': books,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'library/view_books.html', context)


@admin_required
def edit_book(request, pk):
    """Edit an existing book."""
    book = get_object_or_404(Book, pk=pk)
    old_total = book.total_quantity
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated_book = form.save(commit=False)
            # Adjust available quantity when total changes
            diff = updated_book.total_quantity - old_total
            updated_book.available_quantity = max(0, book.available_quantity + diff)
            updated_book.save()
            messages.success(request, f'"{updated_book.title}" updated successfully!')
            return redirect('view_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form, 'book': book})


@admin_required
def delete_book(request, pk):
    """Delete a book from the library."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" deleted successfully!')
        return redirect('view_books')
    return render(request, 'library/delete_book.html', {'book': book})


# ── Category Management ───────────────────────────────────────

@admin_required
def manage_categories(request):
    """Add and list categories."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'library/manage_categories.html', {
        'form': form, 'categories': categories,
    })


@admin_required
def delete_category(request, pk):
    """Delete a category."""
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted!')
        return redirect('manage_categories')
    return redirect('manage_categories')


# ── Student Management ─────────────────────────────────────────

@admin_required
def view_students(request):
    """List all registered students."""
    query = request.GET.get('q', '')
    students = StudentProfile.objects.select_related('user')
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(enrollment_no__icontains=query)
        )
    return render(request, 'library/view_students.html', {
        'students': students, 'query': query,
    })


# ── Issue Management (Admin) ──────────────────────────────────

@admin_required
def issue_book_admin(request):
    """Admin issues a book to a student."""
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            student = form.cleaned_data['student']
            if book.available_quantity < 1:
                messages.error(request, 'No copies available for this book.')
            else:
                issue = IssuedBook.objects.create(
                    book=book,
                    student=student,
                    due_date=timezone.now() + timedelta(days=settings.ISSUE_DURATION_DAYS),
                )
                book.available_quantity -= 1
                book.save()
                messages.success(
                    request,
                    f'"{book.title}" issued to {student.get_full_name()}.'
                )
                # Email notification
                try:
                    send_mail(
                        subject=f'Book Issued: {book.title}',
                        message=(
                            f'Hi {student.first_name},\n\n'
                            f'The book "{book.title}" has been issued to you.\n'
                            f'Due Date: {issue.due_date.strftime("%d %b %Y")}\n\n'
                            f'Please return it on time to avoid fines.\n\n'
                            f'College Library'
                        ),
                        from_email='library@college.edu',
                        recipient_list=[student.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass
                return redirect('view_issued_books')
    else:
        form = IssueBookForm()
    return render(request, 'library/issue_book_admin.html', {'form': form})


@admin_required
def view_issued_books(request):
    """View all issued and returned books."""
    status_filter = request.GET.get('status', '')
    issues = IssuedBook.objects.select_related('book', 'student')
    if status_filter:
        issues = issues.filter(status=status_filter)

    # Update overdue statuses
    for issue in issues:
        if issue.status == 'ISSUED' and issue.is_overdue:
            issue.status = 'OVERDUE'
            issue.fine = issue.calculated_fine
            issue.save()

    return render(request, 'library/view_issued_books.html', {
        'issues': issues, 'status_filter': status_filter,
    })


@admin_required
def return_book_admin(request, pk):
    """Admin processes a book return."""
    issue = get_object_or_404(IssuedBook, pk=pk)
    if issue.status == 'RETURNED':
        messages.info(request, 'This book has already been returned.')
        return redirect('view_issued_books')

    issue.return_date = timezone.now()
    issue.status = 'RETURNED'
    issue.fine = issue.calculated_fine
    issue.save()

    # Restore book availability
    issue.book.available_quantity += 1
    issue.book.save()

    messages.success(
        request,
        f'"{issue.book.title}" returned by {issue.student.get_full_name()}. '
        f'Fine: ₹{issue.fine}'
    )
    # Email notification for return
    try:
        send_mail(
            subject=f'Book Returned: {issue.book.title}',
            message=(
                f'Hi {issue.student.first_name},\n\n'
                f'The book "{issue.book.title}" has been marked as returned.\n'
                f'Fine: ₹{issue.fine}\n\n'
                f'Thank you!\nCollege Library'
            ),
            from_email='library@college.edu',
            recipient_list=[issue.student.email],
            fail_silently=True,
        )
    except Exception:
        pass
    return redirect('view_issued_books')


# ═══════════════════════════════════════════════════════════════
#  STUDENT VIEWS
# ═══════════════════════════════════════════════════════════════

@student_required
def student_dashboard(request):
    """Student dashboard with personal statistics."""
    my_issues = IssuedBook.objects.filter(
        student=request.user, status__in=['ISSUED', 'OVERDUE']
    ).select_related('book')
    total_issued = IssuedBook.objects.filter(student=request.user).count()
    currently_issued = my_issues.count()
    returned = IssuedBook.objects.filter(
        student=request.user, status='RETURNED'
    ).count()
    total_fine = IssuedBook.objects.filter(
        student=request.user
    ).aggregate(total=Sum('fine'))['total'] or 0

    # Update overdue
    for issue in my_issues:
        if issue.is_overdue and issue.status != 'OVERDUE':
            issue.status = 'OVERDUE'
            issue.fine = issue.calculated_fine
            issue.save()

    context = {
        'my_issues': my_issues,
        'total_issued': total_issued,
        'currently_issued': currently_issued,
        'returned': returned,
        'total_fine': total_fine,
    }
    return render(request, 'library/student_dashboard.html', context)


@student_required
def search_books(request):
    """Students can browse and search the book catalog."""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    books = Book.objects.select_related('category')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'library/search_books.html', {
        'books': books, 'categories': categories,
        'query': query, 'selected_category': category_id,
    })


@student_required
def request_issue(request, pk):
    """Student requests to issue a book."""
    book = get_object_or_404(Book, pk=pk)
    if not book.is_available:
        messages.error(request, 'Sorry, this book is not available right now.')
        return redirect('search_books')

    # Check if student already has this book
    existing = IssuedBook.objects.filter(
        book=book, student=request.user, status__in=['ISSUED', 'OVERDUE']
    ).exists()
    if existing:
        messages.warning(request, 'You already have this book issued.')
        return redirect('my_books')

    # Issue the book
    issue = IssuedBook.objects.create(
        book=book,
        student=request.user,
        due_date=timezone.now() + timedelta(days=settings.ISSUE_DURATION_DAYS),
    )
    book.available_quantity -= 1
    book.save()

    messages.success(
        request,
        f'"{book.title}" issued successfully! Due: {issue.due_date.strftime("%d %b %Y")}'
    )
    # Email notification
    try:
        send_mail(
            subject=f'Book Issued: {book.title}',
            message=(
                f'Hi {request.user.first_name},\n\n'
                f'You have issued "{book.title}".\n'
                f'Due Date: {issue.due_date.strftime("%d %b %Y")}\n\n'
                f'Happy Reading!\nCollege Library'
            ),
            from_email='library@college.edu',
            recipient_list=[request.user.email],
            fail_silently=True,
        )
    except Exception:
        pass
    return redirect('my_books')


@student_required
def my_books(request):
    """Show books currently issued to the student."""
    issues = IssuedBook.objects.filter(
        student=request.user, status__in=['ISSUED', 'OVERDUE']
    ).select_related('book')

    for issue in issues:
        if issue.is_overdue:
            issue.status = 'OVERDUE'
            issue.fine = issue.calculated_fine
            issue.save()

    return render(request, 'library/my_books.html', {'issues': issues})


@student_required
def issue_history(request):
    """Full issue history for the student."""
    issues = IssuedBook.objects.filter(
        student=request.user
    ).select_related('book')
    return render(request, 'library/issue_history.html', {'issues': issues})


@student_required
def book_detail(request, pk):
    """Detailed view of a single book."""
    book = get_object_or_404(Book, pk=pk)
    already_issued = IssuedBook.objects.filter(
        book=book, student=request.user, status__in=['ISSUED', 'OVERDUE']
    ).exists()
    return render(request, 'library/book_detail.html', {
        'book': book, 'already_issued': already_issued,
    })
