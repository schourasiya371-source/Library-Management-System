# 📚 College Library Management System

A modern, full-featured Library Management System built with **Django** and **SQLite** — perfect for college projects and resume building.

---

## ✨ Features

### 🔐 Authentication
- Student Registration with enrollment details
- Unified Login (Student & Admin)
- Role-based access control

### 📖 Book Management (Admin)
- Add, Edit, Delete books
- Book cover image upload
- Category management
- Quantity & availability tracking

### 🎓 Student Features
- Browse & search book catalog
- Issue books instantly
- View currently issued books
- Full issue history
- Fine tracking

### 📊 Admin Dashboard
- Total books, copies, students, categories
- Currently issued & overdue books
- Fine collection summary
- Recent issues overview
- Quick action shortcuts

### ⚡ Advanced Features
- **Fine Calculation**: ₹2/day after due date (configurable)
- **Due Date System**: 14-day issue period (configurable)
- **Book Availability**: Real-time stock tracking
- **Email Notifications**: Issue, return, and welcome emails

---

## 🛠️ Tech Stack

| Layer     | Technology                   |
|-----------|------------------------------|
| Backend   | Django 4.2                   |
| Frontend  | HTML, CSS, Bootstrap 5, JS   |
| Database  | SQLite                       |
| Icons     | Bootstrap Icons              |
| Fonts     | Google Fonts (Inter)         |

---

## 📁 Project Structure

```
library_management/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── library_project/         # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── library/                 # Main app
│   ├── models.py            # Category, Book, StudentProfile, IssuedBook
│   ├── views.py             # All views (Auth, Admin, Student)
│   ├── forms.py             # StudentSignup, Book, IssueBook, Category forms
│   ├── urls.py              # URL routing
│   ├── admin.py             # Django admin registration
│   ├── decorators.py        # @admin_required, @student_required
│   ├── templatetags/        # Custom template filters
│   ├── migrations/
│   └── templates/library/   # All HTML templates
├── static/
│   ├── css/style.css        # Custom styles
│   └── js/main.js           # Client-side JavaScript
└── media/                   # Uploaded images
```

---

## 🚀 Setup Guide (Step by Step)

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\RISHABH\.gemini\antigravity\scratch\library_management
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations library
python manage.py migrate
```

### Step 5: Create Admin Superuser
```bash
python manage.py createsuperuser
```
Enter your admin username, email, and password when prompted.

### Step 6: Start Development Server
```bash
python manage.py runserver
```

### Step 7: Open in Browser
- **Home Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Sign Up**: http://127.0.0.1:8000/signup/
- **Django Admin**: http://127.0.0.1:8000/django-admin/

---

## 👤 Default Credentials

After running `createsuperuser`, log in with those credentials.  
The admin account has access to the Admin Dashboard.  
Students can register via the Sign Up page.

---

## ⚙️ Configuration

Edit `library_project/settings.py`:

| Setting              | Default | Description                         |
|----------------------|---------|-------------------------------------|
| `FINE_PER_DAY`       | 2       | Fine amount in ₹ per overdue day    |
| `ISSUE_DURATION_DAYS`| 14      | Days a book can be borrowed          |
| `EMAIL_BACKEND`      | Console | Switch to SMTP for real emails       |

---

## 📸 Key Pages

| Page               | URL                          | Access  |
|--------------------|------------------------------|---------|
| Home               | `/`                          | Public  |
| Login              | `/login/`                    | Public  |
| Sign Up            | `/signup/`                   | Public  |
| Admin Dashboard    | `/admin-dashboard/`          | Admin   |
| Add Book           | `/books/add/`                | Admin   |
| View Books         | `/books/`                    | Admin   |
| Manage Categories  | `/categories/`               | Admin   |
| View Students      | `/students/`                 | Admin   |
| Issue Book         | `/issue-book/`               | Admin   |
| Issued Books       | `/issued-books/`             | Admin   |
| Student Dashboard  | `/student-dashboard/`        | Student |
| Browse Books       | `/search/`                   | Student |
| Book Detail        | `/book/<id>/`                | Student |
| My Books           | `/my-books/`                 | Student |
| Issue History      | `/history/`                  | Student |

---

## 📧 Email Notifications

By default, emails print to the console (development mode).  
To enable real emails, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 📝 License

This project is for educational purposes. Feel free to use and modify.

---

Built with ❤️ using Django & Bootstrap 5
