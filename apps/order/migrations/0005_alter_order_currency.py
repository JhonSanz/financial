# Generated by Django 4.0.2 on 2022-03-22 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(max_length=250),
        ),
    ]
