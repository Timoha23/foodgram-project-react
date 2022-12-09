# Generated by Django 2.2.16 on 2022-12-08 11:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0032_auto_20221208_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='hex_code',
            field=models.CharField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(regex='^#([a-fA-F]|[0-9]){3, 6}$')], verbose_name='Цвет'),
        ),
    ]