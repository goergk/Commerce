# Generated by Django 3.2.3 on 2021-08-19 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_closing_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='category',
            new_name='categories',
        ),
    ]
