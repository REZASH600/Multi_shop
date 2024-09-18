from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from . import forms
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, Http404
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.cart.modules import Cart
from apps.product.models import Product


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = forms.AddressForm
    success_url = reverse_lazy("order_app:checkout")

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        next_page = self.request.GET.get("next")
        if next_page and self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({'url':next_page})
        return super().form_valid(form)


class LoadCitesView(View):
    def get(self, request):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            province_id = request.GET.get("province_id")
            cities = models.City.objects.filter(province_id=province_id).values(
                "id", "name"
            )
            return JsonResponse(list(cities), safe=False)
        return redirect("order_app:get_cities")


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        order = get_object_or_404(models.Order, id=id, is_paid=False)
        return render(request, "order/order.html", {"order": order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(self.request)

        order = models.Order.objects.create(
            user=self.request.user, total_price=cart.total_price_cart()
        )

        try:
            address = models.Address.objects.get(user=self.request.user, is_active=True)
            order.address = address
            order.save()
        except:
            pass

        for item in cart:
            try:
                product = Product.objects.get(id=item["ID"])
                models.OrderItem.objects.create(
                    order=order,
                    product=product,
                    size=item["size"],
                    color=item["color"],
                    quantity=item["quantity"],
                    final_price=item["total"],
                )
            except:
                pass
        cart.clear_cart()
        return redirect("order_app:order_detail", order.id)


class ChangeAddressView(View):
    def post(self, request):
        try:
            order_id = self.request.POST.get("order_id")
            address_id = self.request.POST.get("address_id")
            order = models.Order.objects.get(id=order_id)
            address = models.Address.objects.get(id=address_id)
            address.is_active = True
            address.save()
            order.address = address
            order.save()
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"response": "ok"}, status=200)
            else:
                raise Http404("Page not found.")

        except:
            return redirect("cart_app:list_cart")


class RemoveProductOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id, order_item_id):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            order = get_object_or_404(models.Order, id=order_id, user=self.request.user)
            order_item = get_object_or_404(
                models.OrderItem, order=order, id=order_item_id
            )
            order.total_price = float(order.total_price) - float(order_item.final_price)
            order.save()
            order_item.delete()

            return JsonResponse({"total_price": order.total_price})
        return redirect('cart_app:cart_list')
