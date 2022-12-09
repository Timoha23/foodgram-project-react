# Generated by Django 2.2.16 on 2022-12-08 10:32

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0023_auto_20221208_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='ingredientinrecipeamount',
            name='amount_ingredient',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='hex_code',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='Имя тега'),
        ),
    ]