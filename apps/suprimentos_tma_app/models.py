from django.db import models

# Create your models here.
from apps.calendario_app.models import Calendario_Dias
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario


class Requisicao_Atendida_TMA(models.Model):
    cod_req_atendida_tma = models.AutoField(primary_key=True, editable=False, auto_created=True)
    handle_req_pai = models.IntegerField(blank=False, null=False)
    num_req_pai = models.IntegerField(null=True, blank=True)
    data_inclusao = models.DateTimeField(null=True, blank=True)
    data_confirmada = models.DateTimeField(null=True, blank=True)
    data_atendida = models.DateTimeField(null=True, blank=True)
    handle_usu_incluiu = models.IntegerField(null=True, blank=True)
    nome_usu_incluiu = models.CharField(max_length=50, null=True, blank=True)
    handle_comprador = models.IntegerField(null=True, blank=True)
    nome_comprador = models.CharField(max_length=70, null=True, blank=True)
    #handle_prod = models.IntegerField(null=True, blank=True)
    #cod_ref_prod = models.IntegerField(null=True, blank=True)
    #desc_prod = models.CharField(max_length=200, null=True, blank=True)
    handle_familia = models.IntegerField(null=True, blank=True)
    desc_familia = models.CharField(max_length=70, null=True, blank=True)
    status_ordem = models.CharField(max_length=30, null=True, blank=True)
    #planejado = models.CharField(max_length=1, null=True, blank=True)
    chave_busca = models.CharField(max_length=15, null=False, blank=False)
    status_atendimento = models.CharField(max_length=1, null=True, blank=True)
    tma = models.CharField(max_length=15, null=True, blank=True)
    tma_previsto = models.CharField(max_length=15, null=True, blank=True)
    cod_dia_calendario = models.ForeignKey(Calendario_Dias, models.DO_NOTHING, db_column='cod_dia_calendario',
                                           null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_suprimentos_requisicoes_atendidas_tma'#op_suprimentos_requisicoes_atendidas_tma'



