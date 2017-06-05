from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage

from website.forms import UserForm, UserProfileForm, ProductForm, PaymentTypeForm
from website.models import Product, Category, PaymentType, UserProfile, Order


def index(request):
    template_name = 'index.html'
    all_products = Product.objects.all().order_by('-id')[:20]
    return render(request, template_name, {'products': all_products})


def success(request):
    template_name = 'product/success.html'
    return render(request, template_name, {})


def register(request):
    """
    purpose: allow a user to register an account
    author: Helana Nosrat, Kayla Brewer
    args: pulls information from two forms(user_form and profile_form) and sends that information to the database 
        as a POST to the user and userprofile models
    """

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save()
            profile.user = user

            profile.save()
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = UserProfileForm()
        template_name = 'register.html'
        return render(request, template_name,
                      {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


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
        username = request.POST['username']
        password = request.POST['password']
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
    purpose: allows user to list an item for sale by after submitting a form
    author: Dean Smith, Helana Nosrat, Bri Wyatt
    args: request allows Django to see user session data
    """

    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/create.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST

        def post_product(boolean):
            myfile = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            print("photo url", uploaded_file_url)

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
                photo = uploaded_file_url,
                category = c,
            )

            p.save()
            return p

        try:
            if form_data['is_local']:
                print("is local")
                product = post_product(True)
                template_name = 'product/product_detail.html'
                return render(request, template_name, {'product': product})

        except KeyError:
            product = post_product(False)
            template_name = 'product/product_detail.html'
            return render(request, template_name, {'product': product})


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
def user_profile_view(request):
    """
    purpose: gets a user's account information, orders, and payments to display on page
    author: Helana Nosrat & Kayla Brewer
    returns: all data within the userprofile and user model 
    """
    previous_orders = Order.objects.all().filter(user=request.user)
    payment_types = PaymentType.objects.all().filter(user=request.user)
    current_user = request.user
    user_profile = UserProfile.objects.get(user_id=current_user.id)

    template_name = 'user_profile.html'
    return render(request, template_name,
                  {'previous_orders': previous_orders, 'payment_types': payment_types, 'user_profile': user_profile})


def edit_user_profile(request):
    """
    purpose: allow a user to edit this profile information
    author: Helana Nosrat & Kayla Brewer
    returns: all data within the userprofile and user model 
    """
    if request.method == 'POST':
        user_data = request.POST
        current_user = request.user
        current_user.first_name = user_data['first_name']
        current_user.last_name = user_data['last_name']
        current_user.save()
        active_user = UserProfile.objects.get(user_id=current_user.id)
        active_user.phone = user_data['phone']
        active_user.address = user_data['address']
        active_user.save()
        return HttpResponseRedirect('/user_profile')

    else:
        current_user = request.user
        active_user = UserProfile.objects.get(user_id=current_user.id)
        context = {'active_user': active_user}
        template_name = 'edit_user_profile.html'
        return render(request, template_name, context)