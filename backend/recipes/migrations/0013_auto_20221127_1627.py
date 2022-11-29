# Generated by Django 2.2.16 on 2022-11-27 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20221127_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInRecipeAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_ingredient', models.PositiveSmallIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient')),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientInRecipeAmount', to='recipes.Ingredient'),
        ),
        migrations.DeleteModel(
            name='AmountIngredient',
        ),
        migrations.AddField(
            model_name='ingredientinrecipeamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]