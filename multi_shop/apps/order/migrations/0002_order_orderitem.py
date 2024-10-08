# Generated by Django 5.0.7 on 2024-09-16 04:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
        ("product", "0004_couponcode"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "total_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=15, verbose_name="total price"
                    ),
                ),
                ("is_paid", models.BooleanField(default=False, verbose_name="is paid")),
                (
                    "is_discount",
                    models.BooleanField(default=False, verbose_name="is discount"),
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
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s",
                        to="order.address",
                        verbose_name="address",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "ordering": ("-updated_at", "-created_at"),
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("size", models.CharField(max_length=30, verbose_name="size")),
                ("color", models.CharField(max_length=30, verbose_name="color")),
                (
                    "quantity",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="quantity"
                    ),
                ),
                (
                    "final_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="final price"
                    ),
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
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="order.order",
                        verbose_name="order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
                "ordering": ("-updated_at", "-created_at"),
            },
        ),
    ]
