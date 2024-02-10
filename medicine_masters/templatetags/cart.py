from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(i, cart):
    for id in cart:
        if id.product_id == i.product_id:
            return True
    return False

@register.filter(name='cart_qty')
def cart_qty(i, cart):
    for id in cart:
        if id.product_id == i.product_id:
            return id.cart_quantity
    return 0