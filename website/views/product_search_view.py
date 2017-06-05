from django.shortcuts import render

from django.db.models import Q

from website.models import Product


def product_search(request):
    """
    purpose: allows a user to search all products in the database
    author: Kayla Brewer
    args: gets all products, then filters by query (q)
    returns: a filtered list of products that match the query
    """

    all_products = Product.objects.all().order_by("title", "city", "category")
    query = request.GET.get("q")
    template_name = 'product/product_search.html'
    if query:	
        products = all_products.filter(
        Q(title__contains=query) | Q(city__contains=query) | Q(category__name__contains=query)

        ).distinct()
        return render(request, template_name, {'all_products': products})
