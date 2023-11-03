from django.db import models

# Create your models here.
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import Projeto

class Sigla_Status_Disponibilidade_Frota(models.Model):
    cod_sigla = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_sigla = models.CharField(max_length=35, blank=False, null=False)
    sigla = models.CharField(max_length=8, blank=False, null=False)
    class Meta():
        managed = True
        db_table = 'ger_indisp_frota_siglas_status' #op_frota_indisp_siglas_status'


class Grupo_Indisponibilidade(models.Model):
    cod_grupo_indisponibilidade = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_grupo_indisp = models.CharField(max_length=50, null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_indisp_frota_grupo_indisponibilidade'#op_frota_indisp_grupo_indisponibilidade'

class Apontamento_Promax(models.Model):
    cod_apontamento_promax = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_lancamento = models.DateField(auto_now_add=True)
    data_apontamento = models.DateField(blank=False, null=False)
    placa = models.CharField(max_length=7, null=False, blank=False)
    status_placa = models.CharField(max_length=30, null=False, blank=False, default='DISPONÍVEL')
    numero_os = models.CharField(max_length=40, null=True, blank=True)
    justificativa = models.CharField(max_length=300, null=True, blank=True)
    status_lanc = models.CharField(max_length=1, default='S', null=False, blank=False)
    cod_sigla = models.ForeignKey(Sigla_Status_Disponibilidade_Frota, models.DO_NOTHING, db_column='cod_sigla', null=False, blank=False)
    cod_grupo_indisponibilidade = models.ForeignKey(Grupo_Indisponibilidade, models.DO_NOTHING, db_column='cod_grupo_indisponibilidade', null=True, blank=True)
    cod_projeto =  models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_indisp_frota_apontamento_promax'#op_frota_indisp_apontamento_promax'


class Frota_Contratada(models.Model):
    cod_frota_contratada = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_lancamento = models.DateField(auto_now_add=True)
    data_ref = models.DateField(null=False, blank=False)
    #chave_busca = models.CharField(max_length=15, null=False, blank=False)
    #Campo utilizado somente quando se tratar de empilhadeiras, usar : D(Dia Inteiro), M(manhã), T(tarde), N(noite)
    turno = models.CharField(max_length=1, null=True, blank=True, default='D')
    dia_semana = models.IntegerField(null=False, blank=False, default=0)
    qtd_frota_contratada_ativa = models.IntegerField(null=False, blank=False)
    qtd_frota_contratada_parada = models.IntegerField(null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_indisp_frota_contratada'#op_frota_indisp_contratada'
