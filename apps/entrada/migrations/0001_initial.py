# Generated by Django 5.1.6 on 2025-03-22 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_entrada', models.IntegerField(auto_created=True, default=100)),
            ],
        ),
    ]
