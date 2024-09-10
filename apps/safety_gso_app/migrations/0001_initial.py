

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('safety_checks_aplicados_app', '0002_auto_20240830_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gabarito_GSO',
            fields=[
                ('cod_gabarito_onibus_check', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('placa_onibus', models.CharField(max_length=10)),
                ('cod_check_aplicado', models.ForeignKey(db_column='cod_check_aplicado', on_delete=django.db.models.deletion.DO_NOTHING, to='safety_checks_aplicados_app.Check_Aplicado')),
            ],
            options={
                'db_table': 'op_safe_gso',
                'managed': True,
            },
        ),
    ]
