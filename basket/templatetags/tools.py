from django import template

register = template.Library()

@register.filter(name='discount')
def discount(value, arg):
    """ Applies a percentage discount of arg to input value """
    try:
        return float(value) * (100-float(arg)) / 100
    except (ValueError, TypeError):
        return ''

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """ """
    try:
        return float(price)* float(quantity)
    except (ValueError, TypeError):
        return ''
    
