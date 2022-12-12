# Generated by Django 2.2.16 on 2022-12-12 08:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0033_auto_20221208_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipeamount',
            name='amount_ingredient',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='hex_code',
            field=models.CharField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(regex='^#[a-fA-F0-9]{6}$')], verbose_name='Цвет'),
        ),
    ]
