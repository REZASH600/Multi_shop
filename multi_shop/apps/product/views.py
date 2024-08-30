from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from . import models
from . import forms
from django.http import JsonResponse



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
