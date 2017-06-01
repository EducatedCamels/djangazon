from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

from website.forms import UserForm, UserProfileForm
from website.models import User, Order, Customer


def customer_view(request):
    """
    purpose:
    author: Helana Nosrat
    args: request allows Django to see user session data
    returns:
    the request with that rendered text.
    """

    if request.method == 'GET':
        user_profile_form = UserProfileForm()
        template_name = 'user_profile.html'
        return render(request, template_name, {'user_profile_form': user_profile_form})
    elif request.method == 'POST':
        form_data = request.POST,
        up = UserProfile(
            user = request.user,
            address = form_data['address'],
            phone = form_data['phone'],
        )
        up.save(commit=False)
        template_name = 'edit_user.html'
        return render(request, template_name, {'user_profile': form_data})
        # if user_profile_form.is_valid():
        #     user_profile = user_profile_form.save()

    user_profile = UserProfile.objects.all


    return render(request, template_name, {'user_profile': user_profile})

# def get_order(request):
#     """
#     purpose: Gets user open order or creates a new order.
#     author: Helana Nosrat
#     args: request allows Django to see user session data
#     """
#     user = request.user
#     user_order = Order.objects.get(payment_type_id = None, user_id = user.id)
#     return user_order
#     print("order", user_order)
