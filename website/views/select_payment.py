from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

from website.forms import UserForm
from website.models import PaymentType, Order


def all_payment_types(request):
    """
    purpose: gets users payment types and posts payment type to user open order.
    author: James Tonkin
    args: request allows Django to see user session data
    returns: Combines list_payment.html with all_payment_types dictionary and returns the request with that rendered text.
    """
    if request.method == "GET":
        user = request.user
        all_payment_types = PaymentType.objects.filter(user_id=user.id)
        template_name = 'list_payment.html'
        payment_type_dict = {'all_payment_types': all_payment_types}
        return render(request, template_name, payment_type_dict)

    elif request.method == 'POST':
        user_order = Order.objects.get_or_create(payment_type_id = None, user_id = user.id)
