# Generated by Django 5.0.7 on 2025-03-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sku', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sufixo',
            name='sufixo',
            field=models.CharField(max_length=100),
        ),
    ]
