from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

from website.forms import ProductForm
from website.forms import UserForm
from website.models import Product, Order, LineItem


def shopping_cart(request):
    """
    purpose: gets a line item order to be viewed on shopping_cart.html
    author: Helana Nosrat
    args: request allows Django to see user session data
    returns: Combines product_detail.html with product dictionary and returns
    the request with that rendered text.
    """
    user = request.user
    user_order = Order.objects.get_or_create(payment_type_id = None, user_id = user.id)
    template_name = 'shopping_cart.html'

    products_on_order = LineItem.objects.all().filter(order_id = user_order[0].id)
    print('Products on order: ', products_on_order[0])
    total = 0
    for product_price in products_on_order:
        total += product_price.product.price
    return render(request, template_name, {'products_on_order': products_on_order, 'total': total})
