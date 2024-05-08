from django.db import models

from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado


class Relato(models.Model):
    cod_relato_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_tipo_relato = models.IntegerField(blank=False, null=False)
    situacao_envolvido = models.IntegerField(blank=False, null=False)
    local_relato = models.CharField(max_length=70, blank=False, null=False)
    turno_relato = models.IntegerField(blank=False, null=False)
    atividade_relato = models.IntegerField(blank=False, null=False)
    processo_relato = models.IntegerField(blank=False, null=False)
    cod_checks_aplicados = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_relatos'
