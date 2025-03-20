# Generated by Django 5.0.7 on 2025-03-20 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0001_initial'),
        ('produto', '0002_alter_produto_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='responsavel_pecas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_pecas', to='funcionario.funcionario'),
        ),
    ]
