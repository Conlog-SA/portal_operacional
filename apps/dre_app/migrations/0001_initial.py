

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario_app', '0005_liberacao_usuario_projeto_benner_cod_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layout_Dre',
            fields=[
                ('cod_lay_dre', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('desc_lay', models.CharField(max_length=80)),
                ('ini_vigencia', models.DateField()),
                ('fim_vigencia', models.DateField(blank=True, null=True)),
                ('cod_usu', models.ForeignKey(db_column='cod_usu', on_delete=django.db.models.deletion.DO_NOTHING, to='usuario_app.Usuario')),
            ],
            options={
                'db_table': 'op_dre_layout',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estrutura_Dre',
            fields=[
                ('cod_str_dre', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=80)),
                ('cod_nivel', models.IntegerField()),
                ('cod_str_dre_pai', models.IntegerField(default=0)),
                ('eh_ultimo_nivel', models.CharField(default=False, max_length=1)),
                ('ini_vigencia', models.DateField()),
                ('fim_vigencia', models.DateField(blank=True, null=True)),
                ('cod_lay_dre', models.ForeignKey(db_column='cod_lay_dre', on_delete=django.db.models.deletion.DO_NOTHING, to='dre_app.Layout_Dre')),
                ('cod_usu', models.ForeignKey(db_column='cod_usu', on_delete=django.db.models.deletion.DO_NOTHING, to='usuario_app.Usuario')),
            ],
            options={
                'db_table': 'op_dre_estrutura',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Dre_Contas_Benner',
            fields=[
                ('cod_dre_conta_benner', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('handle_conta', models.IntegerField()),
                ('desc_conta', models.CharField(max_length=80)),
                ('cod_str_dre', models.ForeignKey(db_column='cod_str_dre', on_delete=django.db.models.deletion.DO_NOTHING, to='dre_app.Estrutura_Dre')),
            ],
        ),
    ]
