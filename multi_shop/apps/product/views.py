from typing import Any
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView, View
from . import models
from . import forms
from django.http import JsonResponse, Http404
from . import modules
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.order.models import Order
from django.core.exceptions import ValidationError


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
                    "urlLike": reverse(
                        "product_app:like", kwargs={"product_id": product.id}
                    ),
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


class LikeView(ListView):

    def get(self, request, product_id):

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            if not self.request.user.is_authenticated:
                return JsonResponse(
                    {
                        "url": f"{reverse('account_app:login')}?next={request.GET.get('current_url')}"
                    }
                )

            try:
                obj_like = models.Like.objects.get(
                    user=self.request.user, product_id=product_id
                )
                obj_like.delete()
                is_liked = False

            except:
                models.Like.objects.create(
                    user=self.request.user, product_id=product_id
                )
                is_liked = True

            finally:
                number_like = models.Like.objects.filter(user=self.request.user).count()
                return JsonResponse(
                    {"isLiked": is_liked, "numberLike": number_like}, status=200
                )

        raise Http404()


class HomeView(TemplateView):

    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["offers"] = [
            offer
            for offer in models.Offer.objects.filter(is_publish=True)
            if offer.is_active()
        ][:10]

        context["categories"] = models.Category.objects.filter(is_publish=True)[:12]
        context["recent_products"] = models.Product.objects.filter(is_publish=True)[:12]
        context["brands"] = models.Brand.objects.filter(is_publish=True)[:12]

        return context


class CouponCodeView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        unique_name = self.request.POST.get("unique_name")
        try:
            coupon_code = models.CouponCode.objects.get(name=unique_name)
            order = Order.objects.get(user=self.request.user, id=order_id)
            coupon_code.is_valid(order)
            order.total_price = coupon_code.apply_discount(order)
            order.is_discount = True
            order.save()
            coupon_code.quantity -= 1
            return JsonResponse({"total_price": order.total_price}, status=200)
        
        except Order.DoesNotExist:
            return JsonResponse(
                {"error": "order not found.", "href": reverse("cart_app:cart_list")}, status=404
            )
        except models.CouponCode.DoesNotExist:
            return JsonResponse({"error": "There is no discount code with this name."},status=404)

        except ValidationError as e:

            return JsonResponse({"error": list(e)[0]}, status=404)
