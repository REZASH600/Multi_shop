from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import Truncator
from django.core.exceptions import ValidationError
from apps.account.models import User


class Size(models.Model):
    name = models.CharField(_("size"), max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")


class Color(models.Model):
    name = models.CharField(_("color"), max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"), max_length=50, unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subs",
    )
    image = models.ImageField(_("image"), upload_to="products/images")
    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Brand(models.Model):
    name = models.CharField(_("name"), max_length=50)
    image = models.ImageField(_("image"), upload_to="brand/images")
    is_publish = models.BooleanField(_("is publish"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def show_image(self):
        return format_html(f"<image src='{self.image.url}' width='50px' height='50'>")

    show_image.short_description = _("image")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class Product(models.Model):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("K", "Kids"))

    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"), max_length=50, unique=True, blank=True)
    short_information = models.CharField(
        _("short information"), max_length=120, blank=True
    )
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )

    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=0)
    is_publish = models.BooleanField(_("is publish"), default=True)

    category = models.ManyToManyField(
        Category, verbose_name=_("category"), related_name="%(class)s_category"
    )
    color = models.ManyToManyField(
        Color, verbose_name=_("color"), related_name="%(class)s_color", blank=True
    )
    size = models.ManyToManyField(
        Size, verbose_name=_("size"), related_name="%(class)s_size", blank=True
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name=_("brand"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_brand",
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    @property
    def formatted_price(self):
        return f"{self.price:,.2f}"

    def get_best_discounted_price(self):
        active_offers = [
            offer for offer in self.offer_product.all() if offer.is_active()
        ]
        if not active_offers:
            return self.price

        best_discounted_price = self.price
        for offer in active_offers:
            discounted_price = offer.apply_discount(product=self)
            if discounted_price < best_discounted_price:
                best_discounted_price = discounted_price

        return best_discounted_price

    def get_best_offer(self):
        active_offers = [
            offer
            for offer in self.offer_product.filter(is_publish=True)
            if offer.is_active()
        ]

        if not active_offers:
            return None

        best_offer = max(active_offers, key=lambda offer: offer.percent)
        return best_offer

    def __str__(self):
        return f"{self.name} - {self.price} {self.brand.name if self.brand else ''}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", "-price")
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Offer(models.Model):
    product = models.ManyToManyField(
        Product, verbose_name=_("product"), blank=True, related_name="%(class)s_product"
    )
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), null=True, blank=True)
    image = models.ImageField(_("image"), upload_to="offer/images")
    is_publish = models.BooleanField(_("is publish"), default=True)
    percent = models.FloatField(_("percent"))
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def is_active(self):
        now = timezone.now()
        return now >= self.start_time and now <= self.end_time

    def apply_discount(self, product):
        if self.is_active() and product in self.product.all():
            return float(product.price) * (1 - self.percent / 100)
        return product.price

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

    class Meta:
        ordering = ("-percent", "-start_time")
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")


class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="%(class)s_product",
    )
    image = models.ImageField(_("image"), upload_to="products/images")

    def show_image(self):
        return format_html(f"<image src='{self.image.url}' width='50px' height='50'>")

    show_image.short_description = _("image")

    def __str__(self):
        return f"{self.product.name}: {self.image.name.split('/')[-1]}"

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class AdditionalInformation(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="%(class)s_product",
    )
    description = models.TextField(_("description"))

    def __str__(self):
        truncated_description = Truncator(self.description).chars(50, truncate="...")
        return f"{self.product.name}: {truncated_description}"

    class Meta:
        verbose_name = _("Additional Information")
        verbose_name_plural = _("Additional Informations")


class QuestionAnswer(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="%(class)s_product",
    )
    is_publish = models.BooleanField(_("is publish"), default=True)
    question = models.CharField(_("question"), max_length=50)
    answer = models.CharField(_("answer"), max_length=100)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        truncated_answer = Truncator(self.answer).chars(50, truncate="...")
        return f"{self.question}: {truncated_answer}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Question Answer")
        verbose_name_plural = _("Question Answers")


class Like(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="%(class)s_user",
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="%(class)s_product",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} liked {self.product.name}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="%(class)s_user",
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="%(class)s_product",
    )
    is_publish = models.BooleanField(_("is publish"), default=True)
    message = models.CharField(_("message"), max_length=120)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        truncated_message = Truncator(self.message).chars(50, truncate="...")
        return f"{self.user.phone} wrote '{truncated_message}' for {self.product.name} product"

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class CouponCode(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    percent = models.FloatField(_("percent"))
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    quantity = models.PositiveBigIntegerField(_("quantity"), default=1)
    minimum_purchase = models.DecimalField(
        _("minimum purchase"), max_digits=12, decimal_places=2
    )
    is_active = models.BooleanField(_("is active"), default=True)

    user = models.ManyToManyField(
        User, related_name="coupon_code", verbose_name=_("user")
    )

    product = models.ManyToManyField(
        Product, related_name="coupon_code", verbose_name=_("product")
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def is_valid(self, order):

        now = timezone.now()
        if not (self.start_time <= now <= self.end_time):
            raise ValidationError(
                "This discount is either not yet valid or has expired."
            )

        if not self.is_active:
            raise ValidationError("This discount is inactive.")

        if self.quantity == 0:
            raise ValidationError("This discount has been fully used.")

        if order.total_price < self.minimum_purchase:
            raise ValidationError(
                f"The minimum purchase required for this discount is {self.minimum_purchase}."
            )

        if order.is_discount:
            raise ValidationError("A discount has already been applied to this order.")

        return True

    def apply_discount(self, order):
        total_price = float(order.total_price)
        return total_price - total_price * (1 - self.percent / 100)
    

    def __str__(self):
        return f"{self.name} - {self.percent}%"

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = _("Coupon Code")
        verbose_name_plural = _("Coupon Codes")
