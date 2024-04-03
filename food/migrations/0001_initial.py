# Generated by Django 4.2.11 on 2024-03-28 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="item",
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
                ("item_name", models.CharField(max_length=200)),
                ("item_description", models.CharField(max_length=500)),
                ("item_price", models.IntegerField()),
            ],
        ),
    ]