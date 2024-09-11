from django.shortcuts import render, redirect, reverse
from django.views import View
from . import modules
from apps.product import models
from django.http import JsonResponse


class CartView(View):

    def get(self, request):
        cart = modules.Cart(self.request)
        return render(request, "cart/cart.html", {"cart": cart})

    def post(self, request):
        size = request.POST.get("size")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        product_slug = request.POST.get("slug")
        product = models.Product.objects.get(slug=product_slug)
        cart = modules.Cart(self.request)
        cart.add(product, size, color, quantity)
        return JsonResponse({"url": reverse("cart_app:list_cart")}, status=200)


class RemoveProductView(View):
    def get(self, request, unique_name):

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            cart = modules.Cart(self.request)
            cart.remove_product(unique_name)
            return JsonResponse({"totalCart": cart.total_price_cart()}, status=200)
        return redirect("cart_app:list_cart")


class AddSubtractQuantityView(View):

    def get(self, request, unique_name, value):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            obj_cart = modules.Cart(self.request)
            obj_cart.add_subtract_quantity_product(unique_name, int(value))
            product = obj_cart.cart[unique_name]
            total_price = product["price"] * product["quantity"]
            return JsonResponse(
                {
                    "totalCart": f"{obj_cart.total_price_cart():,.2f}",
                    "totalPrice": f"${total_price:,.2f}",
                },
                status=200,
            )
        return redirect("cart_app:list_cart")
