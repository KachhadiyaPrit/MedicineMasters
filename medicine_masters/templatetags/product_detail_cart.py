from django import template

register = template.Library()

@register.filter(name='is_in_cart_product_detail')
def is_in_cart_product_detail(product, cart):
    for id in cart:
        if id.product_id == product.product_id:
            return True
    return False

@register.filter(name='product_detail_cart')
def product_detail_cart(product, cart):
    for id in cart:
        if id.product_id == product.product_id:
            return id.cart_quantity
    return 0