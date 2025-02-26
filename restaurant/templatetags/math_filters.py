# your_app/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """value ni arg ga ko'paytiradi"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    