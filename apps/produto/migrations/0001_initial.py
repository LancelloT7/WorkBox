# Generated by Django 5.1.6 on 2025-03-22 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('funcionario', '0001_initial'),
        ('pecas', '0001_initial'),
        ('sku', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ENTRADA', 'ENTRADA'), ('TRIAGEM', 'TRIAGEM'), ('CONSERTO', 'CONSERTO'), ('VERIFICAR DISPONIBILIDADE', 'VERIFICAR DISPONIBILIDADE'), ('AGUARDANDO PEÇA', 'AGUARDANDO PEÇA'), ('LIBERADO PARA CONSERTO', 'LIBERADO PARA CONSERTO'), ('EMBALAGEM', 'EMBALAGEM'), ('EMBALADO', 'EMBALADO'), ('ENCERRADO', 'ENCERRADO')], default='ENTRADA', max_length=30)),
                ('data_saida', models.DateTimeField(blank=True)),
                ('registro_saida', models.CharField(blank=True, max_length=100)),
                ('data_entrada', models.DateTimeField(auto_now_add=True)),
                ('observacao', models.CharField(blank=True, max_length=100)),
                ('ptn', models.CharField(max_length=15)),
                ('serie', models.CharField(max_length=30)),
                ('defeito', models.CharField(choices=[('Estético', 'Estético'), ('Funcional', 'Funcional'), ('Estético-Funcional', 'Estético-Funcional'), ('Sem Defeito', 'Sem Defeito'), ('Venda Direta', 'Venda Direta')], max_length=30)),
                ('defeito_especifico', models.CharField(choices=[('Tela Quebrada', 'Tela Quebrada'), ('Não liga', 'Não liga'), ('Sem Defeito', 'Sem Defeito')], default='Sem Defeito', max_length=30)),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_modelo_sku', to='sku.sku')),
                ('pecas', models.ManyToManyField(through='pecas.ProdutoPeca', to='pecas.peca')),
                ('responsavel_conserto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_conserto', to='funcionario.funcionario')),
                ('responsavel_embalagem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_embalagem', to='funcionario.funcionario')),
                ('responsavel_entrada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_entrada', to='funcionario.funcionario')),
                ('responsavel_pecas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_pecas', to='funcionario.funcionario')),
                ('responsavel_saida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_saida', to='funcionario.funcionario')),
                ('responsavel_triagem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsavel_triagem', to='funcionario.funcionario')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_sku', to='sku.sku')),
                ('sufixo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_sufixo', to='sku.sufixo')),
            ],
        ),
    ]
