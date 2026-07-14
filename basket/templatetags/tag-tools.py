from django import template

register = template.Library()

@register.filter
def discount(value, arg):
    """ Applies a percentage discount of arg to input value """
    try:
        return float(value) * (100-float(arg)) / 100
    except (ValueError, TypeError):
        return ''
