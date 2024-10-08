# Generated by Django 5.0.7 on 2024-09-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="offer",
            options={
                "ordering": ("-percent", "-start_time"),
                "verbose_name": "Offer",
                "verbose_name_plural": "Offers",
            },
        ),
        migrations.AddField(
            model_name="offer",
            name="image",
            field=models.ImageField(
                null=True, upload_to="offer/images", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "Female"), ("K", "Kids")],
                max_length=1,
                null=True,
                verbose_name="gender",
            ),
        ),
    ]
