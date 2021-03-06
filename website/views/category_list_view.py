from django.shortcuts import render
from website.models import Category


def category_list(request):
    """purpose: pulls up "category" view listing all product categories
    author: Bri Wyatt
    args: request allows Django to see user session data
    returns: Uses template from product/category_list.html and pulls model data
    from the Category and Product class to return the request with a view of
    that rendered text.
    """
    template_name = 'product/category_list.html'
    categories = Category.objects.all()
    for i in categories:
        print(i)
    cat_dict = {'categories': categories}
    return render(request, template_name, cat_dict)
