from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin


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
