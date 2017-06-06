from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from website.forms import UserForm
from website.models import PaymentType, Order



def delete_payment(request):
	"""
    purpose: allows user to delete a payment type when not in use.
    author: James Tonkin, Dean Smith
    args: request allows Django to see user session data
          product_id is used to generate the individual product
    returns: HttpResponseRedirct to allow user to be view a new url that was not previously specified. Returning
    render to use request, template_name and payment_type_dict all together.
    """

	if request.method == "GET":
		user = request.user
		all_payment_types = PaymentType.objects.filter(user_id=user.id, enabled=1)
		template_name = 'user_payment_options.html'
		payment_type_dict = {'all_payment_types': all_payment_types}
		return render(request, template_name, payment_type_dict)

	elif request.method == 'POST':
		payment_id = request.POST['delete_payment']
		print('---------------------------')
		print(payment_id)
		print('---------------------------')
		payment_is_on_order = Order.objects.filter(
			user_id=request.user,
			payment_type=payment_id
		)

		if not payment_is_on_order:
			PaymentType.objects.filter(pk=payment_id).delete()
			return HttpResponseRedirect('/user_payment_options')

		else:
			payment_is_used = PaymentType.objects.get(pk=payment_id)
			payment_is_used.enabled = 0
			payment_is_used.save()
			return HttpResponseRedirect('/user_payment_options')
