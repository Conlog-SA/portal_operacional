

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estrut_org_app', '0004_filial_tem_calculo_rv'),
        ('usuario_app', '0005_liberacao_usuario_projeto_benner_cod_empresa'),
        ('usuario_app', '0005_liberacao_usuario_projeto_benner_cod_empresa'),
        ('estrut_org_app', '0004_filial_tem_calculo_rv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verbas_Senior_RV',
            fields=[
                ('cod_verba_senior_rv', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('data_ini', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('tipo_verba', models.IntegerField(blank=True, null=True)),
                ('cod_verba', models.CharField(max_length=3)),
                ('cod_filial', models.ForeignKey(db_column='cod_filial', on_delete=django.db.models.deletion.DO_NOTHING, to='estrut_org_app.Filial')),
                ('cod_usu', models.ForeignKey(db_column='cod_usu', on_delete=django.db.models.deletion.DO_NOTHING, to='usuario_app.Usuario')),
            ],
            options={
                'db_table': 'op_conecta_verbas_senior_rv',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Param_Bonus_Devolucao_RV',
            fields=[
                ('cod_param_bonus_dev_rv', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('data_ini', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('cargo', models.IntegerField()),
                ('perc_meta', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('val_bonus_dev', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('cod_filial', models.ForeignKey(db_column='cod_filial', on_delete=django.db.models.deletion.DO_NOTHING, to='estrut_org_app.Filial')),
                ('cod_usu', models.ForeignKey(db_column='cod_usu', on_delete=django.db.models.deletion.DO_NOTHING, to='usuario_app.Usuario')),
            ],
            options={
                'db_table': 'op_conecta_param_bonus_dev_rv',
                'managed': True,
            },
        ),
    ]
