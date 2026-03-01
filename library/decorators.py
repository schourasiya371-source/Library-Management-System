"""
Custom decorators for role-based access control.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Allow access only to staff/superuser (library admin)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in first.')
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """Allow access only to authenticated students (non-staff users)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in first.')
            return redirect('login')
        if request.user.is_staff or request.user.is_superuser:
            messages.info(request, 'Redirecting to admin dashboard.')
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
