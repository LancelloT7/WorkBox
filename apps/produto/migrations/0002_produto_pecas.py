# Generated by Django 5.0.7 on 2025-03-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pecas', '0001_initial'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='pecas',
            field=models.ManyToManyField(through='pecas.ProdutoPeca', to='pecas.peca'),
        ),
    ]
