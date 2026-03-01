/**
 * College Library Management System — JavaScript
 * Handles dynamic UI interactions and client-side features.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Auto-dismiss alerts after 4 seconds ──────────────────
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // ── Animate elements on scroll ───────────────────────────
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .book-card, .content-card').forEach(function (el) {
        observer.observe(el);
    });

    // ── Confirm delete actions ───────────────────────────────
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // ── Book cover image preview on file input ───────────────
    const coverInput = document.getElementById('id_cover_image');
    if (coverInput) {
        coverInput.addEventListener('change', function () {
            const preview = document.getElementById('cover-preview');
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // ── Active nav link highlight ────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ── Tooltip initialization ───────────────────────────────
    const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggers.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });
});
