# Generated by Django 5.1.6 on 2025-03-22 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('cargo', models.CharField(max_length=100)),
                ('cod', models.CharField(max_length=11)),
            ],
        ),
    ]
