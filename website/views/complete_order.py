from django.shortcuts import render
from django.http import HttpResponseRedirect
from website.models import PaymentType, Order


def complete_order(request):
    """
    purpose: gets users payment types and posts payment type to user open order.
    author: James Tonkin
    args: request allows Django to see user session data
    returns: Combines list_payment.html with all_payment_types dictionary and returns the request with that rendered text.
    """
    if request.method == "GET":
        user = request.user
        all_payment_types = PaymentType.objects.filter(user_id=user.id, enabled=1)
        template_name = 'complete_order.html'
        payment_type_dict = {'all_payment_types': all_payment_types}
        return render(request, template_name, payment_type_dict)

    elif request.method == 'POST':
        form_data = request.POST
        user = request.user
        user_order = Order.objects.get_or_create(
            payment_type_id=None,
            user=request.user
        )
        payment = PaymentType.objects.get(id=form_data["payment_type"])
        user_order[0].payment_type = payment
        user_order[0].save()

        return HttpResponseRedirect('/success')
