from django.shortcuts import render

from django.db.models import Q

from website.models import Product


def product_search(request):

    all_products = Product.objects.all().order_by("title")
    query = request.GET.get("q")
    template_name = 'product/product_search.html'
    if query:
        products = all_products.filter(
        Q(title__contains=query)
        ).distinct()
        return render(request, template_name, {'all_products': products})
