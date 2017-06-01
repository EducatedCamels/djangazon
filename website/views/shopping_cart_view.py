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
    purpose: gets a line item order to be viewed on shopping_cart.html.  Also deletes product from the shopping cart.
    author: Helana Nosrat, James Tonkin
    args: request allows Django to see user session data
    returns: Combines product_detail.html with product dictionary and returns
    the request with that rendered text.
    """
    if request.method == "GET":
        user_order = Order.objects.get_or_create(payment_type_id = None, user_id = request.user.id)
        template_name = 'shopping_cart.html'

        products_on_order = LineItem.objects.all().filter(order_id = user_order[0].id)
        total = 0
        for product_price in products_on_order:
            total += product_price.product.price
        return render(request, template_name, {'products_on_order': products_on_order, 'total': total})

    elif request.method == 'POST':
        line_item_id = request.POST['delete_product']
        order = Order.objects.get(payment_type_id=None, user=request.user)
        delete_product = LineItem.objects.filter(
            pk=line_item_id,
            order=order
        )

        delete_product.delete()
        return HttpResponseRedirect('/shopping_cart')
