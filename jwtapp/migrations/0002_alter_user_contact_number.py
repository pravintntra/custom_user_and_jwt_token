# Generated by Django 3.2.10 on 2021-12-31 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jwtapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="contact_number",
            field=models.IntegerField(null=True),
        ),
    ]
