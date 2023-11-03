from django.db import models

from apps.estrut_org_app.models import Filial


class Calendario(models.Model):
    cod_calendario = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_calendario = models.CharField(max_length=30, null=True, blank=True, default=None)
    ano_calendario = models.IntegerField()
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial')
    class Meta():
        managed = True
        db_table = 'op_calendario'


class Calendario_Dias(models.Model):
    cod_calendario_dia = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_dia = models.DateField(null=False)
    dia_semana = models.IntegerField()
    classificacao_dia = models.CharField(max_length=1, null=False, blank=False)
    qtd_dias_data_prevista_req_e = models.IntegerField(default=0)
    data_prevista_req_e = models.DateField(null=True, default=None)
    qtd_dias_data_prevista_req_ne = models.IntegerField(default=0)
    data_prevista_req_ne = models.DateField(null=True, default=None)
    qtd_dias_data_prevista_req_plan = models.IntegerField(default=0)
    data_prevista_req_plan = models.DateField(null=True, default=None)
    num_semana = models.IntegerField()
    mes_ref_num_semana = models.IntegerField(default=0)
    periodo = models.CharField(max_length=30, null=True, blank=True, default=None)
    mes_competencia_periodo = models.IntegerField(default=0)
    ano_competencia_periodo = models.IntegerField(default=0)
    cod_calendario = models.ForeignKey(Calendario, models.DO_NOTHING, db_column='cod_calendario')
    class Meta():
        managed = True
        db_table = 'op_calendario_dias'