from . import models


def filter_product(request):
    products = models.Product.objects.filter(is_publish=True)

    search = request.GET.get("q")
    if search:
        products = products.filter(name__icontains=search)

    categories = request.GET.getlist("category")
    if categories:
        products = products.filter(category__slug__in=categories).distinct()

    gender = request.GET.get("gender")
    if gender:
        products = products.filter(gender=gender)

    colors = request.GET.getlist("color")
    if colors:
        products = products.filter(color__name__in=colors).distinct()

    sizes = request.GET.getlist("size")
    if sizes:
        products = products.filter(size__name__in=sizes).distinct()

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    offer_id = request.GET.get("offer_id")
    if offer_id:
        try:
            offer = models.Offer.objects.get(id=offer_id)
        except models.Offer.DoesNotExist:
            offer = None

        if offer:
            filtered_product_ids = []
            for product in products:
                best_offer = product.get_best_offer()
                if best_offer and best_offer.id == offer.id:
                    filtered_product_ids.append(product.id)
            products = products.filter(id__in=filtered_product_ids)

    return products
