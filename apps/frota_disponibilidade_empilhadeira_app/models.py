from django.db import models

# Create your models here.
from apps.frota_disponibilidade_app.models import Sigla_Status_Disponibilidade_Frota
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import  Projeto


class Apontamento_Disp_Empilhadeira(models.Model):
    cod_apontamento_disp_emp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    #fields from Benner
    handle_emp_benner = models.IntegerField()
    placa_emp_benner = models.CharField(max_length=10, blank=False, null=False)
    ano_emp_benner = models.IntegerField()
    modelo_emp_benner = models.CharField(max_length=100, blank=True, null=True)
    placa_emp_anterior_benner = models.CharField(max_length=10, blank=True, null=True)
    ativo_benner = models.CharField(max_length=1, blank=False, null=False)
    #fields from note
    data_apontamento = models.DateField(blank=False, null=False)
    dia_semana = models.IntegerField(null=False, blank=False, default=0)
    turno = models.CharField(max_length=1, blank=False, null=False)
    status_lanc = models.CharField(max_length=1, blank=False, null=False, default='A')
    data_lancamento = models.DateField(auto_now_add=True)
    obs = models.CharField(max_length=200, blank=True, null=True)
    #foreign keys
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usuario', null=False, blank=False)
    cod_sigla = models.ForeignKey(Sigla_Status_Disponibilidade_Frota, models.DO_NOTHING, db_column='cod_sigla',
                                  null=True, blank=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_frota_indisp_frota_apontamento_empilhadeiras'#op_frota_indisp_apontamento_empilhadeiras'


class OS_Apontamento_Disp_Empilhadeira(models.Model):
    cod_os_apontamento_disp_emp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    #fields from Benner
    handle_os_benner = models.IntegerField()
    num_os_benner = models.CharField(max_length=20, blank=False, null=False)
    tipo_os_benner = models.IntegerField()
    data_inicial_os_benner = models.DateTimeField(blank=False, null=False)
    data_final_os_benner = models.DateTimeField(blank=False, null=False)
    handle_conjunto_manut_benner = models.IntegerField(blank=True, null=True)
    desc_conj_manut_benner = models.CharField(max_length=50, blank=True, null=True)
    desc_os_benner = models.CharField(max_length=120, blank=True, null=True)
    #dados para auditoria
    motivo = models.CharField(max_length=300, blank=True, null=True)
    parada_ini_aud = models.DateTimeField(blank=True, null=True)
    parada_fim_aud = models.DateTimeField(blank=True, null=True)
    #foreign key
    cod_apontamento_disp_emp = models.ForeignKey(Apontamento_Disp_Empilhadeira, models.DO_NOTHING,
                                                 db_column='cod_apontamento_disp_emp', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_frota_infor_os_empilhadeiras'#op_frota_info_os_empilhadeiras'


class Linha_Excel_Apontamento_Promax_Empilhadeira():
    def __init__(self, data, placa, num_os, justificativa, sigla,
                 projeto, turno, handle_emp, ano_emp, modelo_emp, ativo, status_leitura_importacao):
        self.data = data
        self.placa = placa
        self.num_os = num_os
        self.justificativa = justificativa
        self.sigla = sigla
        self.projeto = projeto
        self.turno = turno
        self.handle_emp = handle_emp
        self.ano_emp = ano_emp
        self.modelo_emp = modelo_emp
        self.ativo = ativo
        self.status_leitura_importacao = status_leitura_importacao





