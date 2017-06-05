from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse

from website.forms import UserForm, UserProfileForm, ProductForm, PaymentTypeForm
from website.models import User, Product, Category, PaymentType, UserProfile

def index(request):
    template_name = 'index.html'
    all_products = Product.objects.all().order_by('-id')[:20]
    return render(request, template_name, {'products': all_products})

def success(request):
    template_name = 'product/success.html'
    return render(request, template_name, {})


# Create your views here.
def register(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        data = request.POST
        user = User.objects.create_user(
            username = data['username'],
            password = data['password'],
            first_name = data['first_name'],
            last_name = data['last_name'],

        )

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save()
            profile.user = user

            profile.save()
            # customer = Customer(pk=user_id[1])
            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = UserProfileForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

def sell_product(request):

    """
    purpose: add a payment type to the data base
    author: Dean Smith, Helana Nosrat
    args: request allows Django to see user session data
    """

    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/create.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST
        print(form_data)

        def post_product(boolean):
            c = Category.objects.get(pk=form_data['category'])
            p = Product(
                seller = request.user,
                title = form_data['title'],
                description = form_data['description'],
                price = form_data['price'],
                quantity = form_data['quantity'],
                is_local = boolean,
                city = form_data['city'],
                date = 'date',
                category = c,
            )
            p.save()
            return p
        try:
            if form_data['is_local']:
                product = post_product(True)
                template_name = 'product/product_detail.html'
                return render(request, template_name, {'product': form_data})

        except KeyError:
            product = post_product(False)
            template_name = 'product/product_detail.html'
            return render(request, template_name, {'product': form_data})

def list_products(request):
    all_products = Product.objects.all()
    template_name = 'product/list.html'
    return render(request, template_name, {'products': all_products})

def add_payment_type(request):

    """
    purpose: add a payment type to the data base
    author: Dean Smith, Helana Nosrat
    args: request allows Django to see user session data
    """

    if request.method == 'GET':
        payment_type_form = PaymentTypeForm()
        template_name = 'add_payment_type.html'
        return render(request, template_name, {'payment_type_form': payment_type_form})

    elif request.method == 'POST':
        form_data = request.POST
        p = PaymentType(
            user=request.user,
            name=form_data['name'],
            account_number=form_data['account_number'],
        )
        p.save()

        return HttpResponseRedirect('/categories')


@login_required
def userprofiles(request):
    """Show all user profiles"""
    userprofiles = UserProfile.objects.filter(owner=request.user)
    template_name = 'user_profile.html'
    if request.method == 'GET':
        return render(request, template_name)

    if request.method == 'POST':
        return render(request, template_name)

# def edit_user_profile(request):
#     """Edit an existing entry"""
#     # user_profile = UserProfile.objects.get(id=user_profile_id)
#     # user = user_profile.user
#
#     if request.method == 'GET':
#         # Intial request; pre-fill form with current entry
#         user_profile_form = EditUserProfileForm(instance=request.user)
#         edit_user_form = UserProfileForm(instance=request.user.user_profile)
#
#         return render(request, "edit_entry.html", {
#             "user_profile_form": user_profile_form,
#             "edit_user_form": edit_user_form,
#         })
#
#     elif request.method == 'POST':
#         user_profile_form = EditUserProfileForm(request.POST, instance=request.user)
#         edit_user_form = UserProfileForm(request.POST, instance=request.user.user_profile)
#         if user_profile_form.is_valid() and edit_user_form.is_valid():
#             user_profile_form.save()
#             edit_user_form = edit_user_form.save(commit=False)
#             edit_user_form.user = request.user
#             edit_user_form.save()
#
#             return HttpResponseRedirect("user_profile")
#
#         else:
#
#             return render(request, "edit_entry.html", {
#                 "user_profile_form": user_profile_form,
#                 "edit_user_form": edit_user_form,
#                 })
