from django.db import models

from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado


class Relato(models.Model):
    cod_relato_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_tipo_relato = models.IntegerField(blank=False, null=False)
    situacao_envolvido = models.IntegerField(blank=True, null=True)
    local_relato = models.CharField(max_length=70, blank=False, null=False)
    atividade_relato = models.IntegerField(blank=True, null=True)
    processo_relato = models.IntegerField(blank=False, null=False)
    categoria_ato_inseguro = models.IntegerField(blank=True, null=True)
    categoria_condicao_insegura = models.IntegerField(blank=True, null=True)
    categoria_comportamento_seguro = models.IntegerField(blank=True, null=True)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_relatos'
