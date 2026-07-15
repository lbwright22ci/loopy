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
    
@register.filter(name='calc_sub_sale')
def calc_sub_sale(rate, args):
    """"""
    price = args.split(',')[0]
    print(price)
    quantity = args.split(',')[1]
    try:
        return float(price)*(100-float(rate))/100 * float(quantity)
    except:
        return ''