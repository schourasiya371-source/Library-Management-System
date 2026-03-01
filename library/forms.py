"""
Forms for user registration, book management, and book issuing.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Category, StudentProfile


class StudentSignupForm(UserCreationForm):
    """Registration form for new students."""
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'Email Address'
        })
    )
    enrollment_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Enrollment Number'
        })
    )
    branch = forms.ChoiceField(
        choices=StudentProfile.BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Phone Number'
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                enrollment_no=self.cleaned_data['enrollment_no'],
                branch=self.cleaned_data['branch'],
                phone=self.cleaned_data.get('phone', ''),
            )
        return user


class BookForm(forms.ModelForm):
    """Form for adding/editing books (admin use)."""

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'category', 'description',
            'cover_image', 'total_quantity', 'publisher', 'edition',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Book Title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Author Name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'ISBN Number'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Brief description of the book'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'total_quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Publisher'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Edition'
            }),
        }


class IssueBookForm(forms.Form):
    """Form for admin to issue a book to a student."""
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available_quantity__gt=0),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select a book'
    )
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_staff=False, is_superuser=False, profile__isnull=False
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select a student'
    )


class CategoryForm(forms.ModelForm):
    """Form for adding/editing categories."""

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Category Description'
            }),
        }
