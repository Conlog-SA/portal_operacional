from django.db import models


class Chamado_Atendido_TMA(models.Model):
    num_chamado = models.IntegerField(primary_key=True, blank=False, null=False)
    nome_usu = models.CharField(max_length=70, null=True, blank=True)
    desc_topico = models.CharField(max_length=80, null=True, blank=True)
    desc_sub_topico = models.CharField(max_length=80, null=True, blank=True)
    aberto_em = models.DateTimeField(null=True, blank=True)
    fechado_em = models.DateTimeField(null=True, blank=True)
    horas_atendimento = models.IntegerField(blank=False, null=False)
    sla = models.IntegerField(blank=False, null=False)
    data_sla = models.DateTimeField(null=True, blank=True)
    login_atendente = models.CharField(max_length=70, null=True, blank=True)
    class Meta():
        managed = True
        db_table = 'op_ti_chamados_atendidos_tma'
