# Generated by Django 4.2.11 on 2024-04-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="item_image",
            field=models.CharField(
                default="https://theme-assets.getbento.com/sensei/5271791.sensei/assets/images/catering-item-placeholder-704x520.png",
                max_length=700,
            ),
        ),
    ]
