# Generated by Django 2.2.16 on 2022-11-27 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20221126_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amountingredient',
            old_name='ingredient_name',
            new_name='ingredient',
        ),
        migrations.RenameField(
            model_name='amountingredient',
            old_name='recipe_name',
            new_name='recipe',
        ),
    ]
