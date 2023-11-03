from django.db import models
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import Filial


# Create your models here.
class Verbas_Erros_de_Pagamentos(models.Model):
    cod_verba = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_verba = models.CharField(max_length=35, null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_gente_gestao_verba' #'op_geg_erros_pagamentos_verbas'

class Erros_de_Pagamento(models.Model):
    cod_erro_pagamento = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_colaborador_senior = models.IntegerField()
    nome_colaborador = models.CharField(max_length=80, null=False, blank=False)
    cod_cargo_senior = models.IntegerField(null=True, blank=True)
    desc_cargo = models.CharField(max_length=80, null=True, blank=True)
    data_admissao = models.DateField(null=True, blank=True)
    mes_competencia = models.DateField()
    valor_erro = models.DecimalField(max_digits=8, decimal_places=2)
    duvida = models.CharField(max_length=300, null=False, blank=False)
    acao = models.CharField(max_length=300, null=False, blank=False)
    nome_responsavel = models.CharField(max_length=30, null=False, blank=False)
    prazo = models.DateField()
    obs = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField()
    status_lancamento = models.CharField(max_length=1, null=False, blank=False, default='S')
    data_lancamento = models.DateField(auto_now_add=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', default=None)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', default=None)
    cod_verba = models.ForeignKey(Verbas_Erros_de_Pagamentos, models.DO_NOTHING, db_column='cod_verba', default=None)
    class Meta():
        managed = True
        db_table = 'ger_gente_gestao_erro_pagamento' #'op_geg_erros_pagamentos'