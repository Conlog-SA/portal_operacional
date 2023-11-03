from django.db import models

class Confirma_Periodo_Fechamento_Folha(models.Model):
    cod_confirma_periodo_fechamento_folha = models.AutoField(primary_key=True, editable=False, blank=False,
                                                             auto_created=True)
    mes_competencia_periodo = models.IntegerField(default=0)
    ano_competencia_periodo = models.IntegerField(default=0)
    ativa = models.CharField(max_length=1, blank=False, null=False)
    class Meta():
        managed = True
        db_table = 'op_plan_controle_confirma_periodo_fecha_folha'


