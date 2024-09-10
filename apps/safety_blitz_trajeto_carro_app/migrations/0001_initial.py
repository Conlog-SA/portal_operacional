

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        ('safety_checks_aplicados_app', '0002_auto_20240830_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blitz_Trajeto_Carro',
            fields=[
                ('cod_blitz_trajeto_carro', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('placa', models.CharField(max_length=20)),
                ('situacao_colaborador', models.IntegerField(blank=True, null=True)),
                ('cod_check_aplicado', models.ForeignKey(db_column='cod_check_aplicado', on_delete=django.db.models.deletion.DO_NOTHING, to='safety_checks_aplicados_app.Check_Aplicado')),
            ],
            options={
                'db_table': 'op_safe_blitz_trajeto_carro',
                'managed': True,
            },
        ),
    ]
