from django.shortcuts import render
from website.models import Category


def single_category(request, category_id):
    """
    purpose: gets a single category and displays all products from that category
    in category_detail.html
    author: James Tonkin
    args: request allows Django to see user session data
          product_id is used to generate the individual product
    returns: Combines single_category.html with category dictionary and returns
    the request with that rendered text.
    """
    category = Category.objects.get(pk=category_id)
    template_name = 'single_category.html'
    return render(request, template_name, {'category': category})
