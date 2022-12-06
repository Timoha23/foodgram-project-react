# Generated by Django 2.2.16 on 2022-11-27 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20221127_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amountingredient',
            old_name='ingredient_name',
            new_name='ingredient',
        ),
        migrations.AlterField(
            model_name='amountingredient',
            name='recipe_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_name', to='recipes.Recipe'),
        ),
    ]
