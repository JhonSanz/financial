# Generated by Django 4.0.2 on 2022-04-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_usd',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]