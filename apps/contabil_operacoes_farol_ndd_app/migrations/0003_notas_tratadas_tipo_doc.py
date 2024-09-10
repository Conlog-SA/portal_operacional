

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabil_operacoes_farol_ndd_app', '0002_excecoes_natureza_operacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='notas_tratadas',
            name='tipo_doc',
            field=models.CharField(blank=True, default='N', max_length=1, null=True),
        ),
    ]
