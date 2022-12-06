# Generated by Django 2.2.16 on 2022-11-29 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20221127_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipeamount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientinrecipe', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientinrecipeamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientinrecipe', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='recipes.Tag'),
        ),
    ]
