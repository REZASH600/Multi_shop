from django import template
from apps.product import models

register = template.Library()


@register.simple_tag
def update_url_param(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)

    if urlencode is not None:
        querystring = urlencode.split("&")
        queryfilter = filter(lambda p: p.split("=")[0] != field_name, querystring)
        query = "&".join(queryfilter)
        url = "{}&{}".format(url, query)

    return url


@register.filter
def is_like(request, product_id):
    try:
        is_liked = models.Like.objects.filter(
            user=request.user, product_id=product_id
        ).exists()

        return is_liked
    except:
        return False
