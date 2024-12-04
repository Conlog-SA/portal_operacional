from django.db import models
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import Atividade

# Create your models here.
class Tipo_Processo(models.Model):
    cod_tipo_processo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_tipo_processo = models.CharField(max_length=80, blank=False, null=False)
    class Meta:
        managed=True
        db_table='op_ti_painel_tipos_processos'


class Status_Exec_Processo(models.Model):
    cod_status_exec_processo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_status_exec_processo = models.CharField(max_length=30, blank=False, null=False)
    class Meta:
        managed=True
        db_table='op_ti_painel_status_exec_processos'


class Processo(models.Model):
    cod_processo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_processo = models.CharField(max_length=60, blank=False, null=False)
    periodicidade= models.CharField(max_length=1, blank=False, null=False) #D - diario/ S - Semanal / M - mensal/ A - anual / H - Hora
    data_desativacao = models.DateField(null=True, blank=True)
    frequencia = models.CharField(max_length=200, blank=False, null=False)
    eh_ativo = models.IntegerField(blank=True, null=True, default=0)
    cod_usu= models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    cod_tipo_processo = models.ForeignKey(Tipo_Processo, models.DO_NOTHING, db_column='cod_tipo_processo',
                                      null=True, blank=True)
    #cod_da_area
    cod_atividade = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='cod_atividade', null=True, blank=True)
    cod_prioridade = models.CharField(max_length=1, blank=False, null=False)
    class Meta:
        managed=True
        db_table='op_ti_painel_processos'

class Execucao_Processo(models.Model):
    cod_exec_processo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    obs_exec_processo = models.CharField(max_length=300, blank=False, null=False)
    data = models.DateField(null=True, blank=True)
    hora_inicio_exec = models.DateTimeField(null=True, blank=True)
    hora_fim_exec = models.DateTimeField(null=True, blank=True)
    cod_status_exec_processo = models.ForeignKey(Status_Exec_Processo, models.DO_NOTHING,
                                                 db_column='cod_status_exec_processo', null=True, blank=True)
    class Meta:
        managed=True
        db_table='op_ti_painel_exec_processos'





