# Generated by Django 3.2.10 on 2022-01-04 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jwtapp", "0007_alter_story_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="story",
            options={"ordering": ("id",), "verbose_name": "story"},
        ),
    ]
