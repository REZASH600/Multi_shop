from apps.product import models


def categories(request):
    context = {"categories": models.Category.objects.filter(is_publish=True)}

    return context
