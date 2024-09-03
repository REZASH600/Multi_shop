from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from . import models
from . import forms
from django.http import JsonResponse
from . import modules
import json


class ProductDetailView(DetailView):
    model = models.Product
    queryset = models.Product.objects.filter(is_publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(models.Product, slug=self.kwargs["slug"])

        categories = product.category.filter(is_publish=True)

        related_products = (
            models.Product.objects.filter(category__in=categories)
            .distinct()
            .exclude(slug=self.kwargs["slug"])
        )
        comments = product.comment_product.filter(is_publish=True)[:6]
        context["related_products"] = related_products
        context["comments"] = comments
        context["max_comments"] = 6
        context["form"] = forms.CommentForm(request=self.request)

        return context

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(models.Product, slug=self.kwargs["slug"])
        form = forms.CommentForm(request.POST, request=self.request, product=product)
        if form.is_valid():
            comment = form.save()
            user = self.request.user

            return JsonResponse(
                {
                    "response": "ok",
                    "imageUrl": user.image.url,
                    "message": form.cleaned_data["message"],
                    "createdAt": comment.created_at.strftime("%d %M %Y"),
                    "name": user.full_name if user.full_name else user.first_name,
                },
                status=200,
            )

        return JsonResponse({"error": form.errors}, status=400)


class ProductListView(ListView):
    model = models.Product
    queryset = models.Product.objects.filter(is_publish=True)
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, self.get_paginate_by(queryset))
        page_number = request.GET.get("page") or 1
        page_obj = paginator.get_page(page_number)

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            saved_list = []
            is_authenticated = self.request.user.is_authenticated
            for product in page_obj.object_list:

                is_liked = models.Like.objects.filter(
                    user=self.request.user if is_authenticated else None,
                    product=product,
                ).exists()

                product_json = {
                    "imageUrl": product.image_product.all().first().image.url,
                    "redirectUrl": reverse(
                        "product_app:detail", kwargs={"slug": product.slug}
                    ),
                    "name": product.name,
                    "price": product.price,
                    "bestDiscountedPrice": product.get_best_discounted_price(),
                    "isLiked": is_liked,
                    "urlLike": "#",
                }

                saved_list.append(product_json)

            pagination_data = {
                "has_other_pages": page_obj.has_other_pages(),
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next(),
                "num_pages": page_obj.paginator.num_pages,
                "current_page": page_obj.number,
                "previous_page_number": (
                    page_obj.previous_page_number() if page_obj.has_previous() else None
                ),
                "next_page_number": (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
            }
            return JsonResponse(
                {"products": saved_list, "pagination": pagination_data}, safe=False
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colors = models.Color.objects.all()
        sizes = models.Size.objects.all()

        selected_colors = self.request.GET.getlist("color")
        selected_sizes = self.request.GET.getlist("size")

        context["colors"] = colors
        context["sizes"] = sizes
        context["selected_colors"] = selected_colors
        context["selected_sizes"] = selected_sizes

        return context

    def get_queryset(self):
        queryset = modules.filter_product(self.request)
        return queryset

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page")
        if per_page is not None and per_page.isdigit():
            self.paginate_by = int(per_page)

        return self.paginate_by
