# Generated by Django 3.2.3 on 2021-08-12 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('toy', 'Toys'), ('cloth', 'Clothes'), ('electronic', 'Electronics'), ('home', 'Home'), ('sport', 'Sport'), ('book', 'Books')], max_length=16)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=2500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_url', models.CharField(blank=True, max_length=500)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('closing_date', models.DateTimeField(blank=True)),
                ('closed', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(related_name='listings', to='auctions.Category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_creators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=2500)),
                ('date', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing')),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=7)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
