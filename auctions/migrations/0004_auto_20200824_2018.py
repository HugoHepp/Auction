# Generated by Django 3.0.8 on 2020-08-25 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='price',
            new_name='current_bid',
        ),
        migrations.AddField(
            model_name='auction',
            name='starting_price',
            field=models.IntegerField(default=0),
        ),
    ]
