"""Custom template tags and filters for the library app."""
from django import template

register = template.Library()


@register.filter
def has_profile(user):
    """Check if a user has a StudentProfile."""
    return hasattr(user, 'profile')
