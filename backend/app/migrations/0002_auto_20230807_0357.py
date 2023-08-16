# Generated by Django 2.2.19 on 2023-08-07 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredienttorecipe',
            options={},
        ),
        migrations.AddConstraint(
            model_name='ingredienttorecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='Ingredient and Recipe in IngredientAmount is unique'),
        ),
    ]