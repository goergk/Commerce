# Generated by Django 3.2.3 on 2021-08-19 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_category_listing_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='categories',
            new_name='category',
        ),
    ]