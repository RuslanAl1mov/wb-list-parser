# Generated by Django 5.2.1 on 2025-06-02 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_alter_productphoto_options_parserhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parserhistory',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parser.product', verbose_name='Скаченый продукт'),
        ),
    ]
