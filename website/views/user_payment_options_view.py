from django.shortcuts import get_object_or_404, render

from website.forms import UserForm
from website.models import PaymentType, Order



def delete_payment(request):

	if request.method == "GET":
		user = request.user
		all_payment_types = PaymentType.objects.filter(user_id=user.id)
		template_name = 'user_payment_options.html'
		payment_type_dict = {'all_payment_types': all_payment_types}
		return render(request, template_name, payment_type_dict)
