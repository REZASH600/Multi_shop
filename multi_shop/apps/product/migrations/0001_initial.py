# Generated by Django 5.0.7 on 2024-08-27 06:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "image",
                    models.ImageField(upload_to="brand/images", verbose_name="image"),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15, verbose_name="color")),
            ],
            options={
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
            },
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=15, verbose_name="size")),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "slug",
                    models.SlugField(blank=True, unique=True, verbose_name="slug"),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="products/images", verbose_name="image"
                    ),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subs",
                        to="product.category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "slug",
                    models.SlugField(blank=True, unique=True, verbose_name="slug"),
                ),
                (
                    "short_information",
                    models.CharField(
                        blank=True, max_length=120, verbose_name="short information"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female")],
                        max_length=1,
                        null=True,
                        verbose_name="gender",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="price"
                    ),
                ),
                ("quantity", models.IntegerField(default=0, verbose_name="quantity")),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_brand",
                        to="product.brand",
                        verbose_name="brand",
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="%(class)s_category",
                        to="product.category",
                        verbose_name="category",
                    ),
                ),
                (
                    "color",
                    models.ManyToManyField(
                        blank=True,
                        related_name="%(class)s_color",
                        to="product.color",
                        verbose_name="color",
                    ),
                ),
                (
                    "size",
                    models.ManyToManyField(
                        blank=True,
                        related_name="%(class)s_size",
                        to="product.size",
                        verbose_name="size",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ("-created_at", "-price"),
            },
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                ("percent", models.FloatField(verbose_name="percent")),
                ("start_time", models.DateTimeField(verbose_name="start time")),
                ("end_time", models.DateTimeField(verbose_name="end time")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "product",
                    models.ManyToManyField(
                        blank=True,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Offer",
                "verbose_name_plural": "Offers",
                "ordering": ("-start_time", "-percent"),
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Like",
                "verbose_name_plural": "Likes",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="products/images", verbose_name="image"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                ("message", models.CharField(max_length=120, verbose_name="message")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
        migrations.CreateModel(
            name="AdditionalInformation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Additional Information",
                "verbose_name_plural": "Additional Informations",
            },
        ),
        migrations.CreateModel(
            name="QuestionAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_publish",
                    models.BooleanField(default=True, verbose_name="is publish"),
                ),
                ("question", models.CharField(max_length=50, verbose_name="question")),
                ("answer", models.CharField(max_length=100, verbose_name="answer")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_product",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question Answer",
                "verbose_name_plural": "Question Answers",
                "ordering": ("-created_at",),
            },
        ),
    ]