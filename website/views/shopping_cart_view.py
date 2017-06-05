from django.shortcuts import render
from website.models import Order, LineItem


def shopping_cart(request):
    """
    purpose: gets a line item order to be viewed on shopping_cart.html
    author: Helana Nosrat
    args: request allows Django to see user session data
    returns: Combines product_detail.html with product dictionary and returns
    the request with that rendered text.
    """
    user = request.user
    user_order = Order.objects.get_or_create(payment_type_id=None, user_id=user.id)
    template_name = 'shopping_cart.html'

    products_on_order = LineItem.objects.all().filter(order_id=user_order[0].id)
    total = 0
    for product_price in products_on_order:
        total += product_price.product.price
    return render(request, template_name, {'products_on_order': products_on_order, 'total': total})
