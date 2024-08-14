from django.db import models

from apps.estrut_org_app.models import Filial, Projeto
from apps.usuario_app.models import Usuario


# Create your models here.
class Param_RV_Rota(models.Model):
    cod_param_rv_rota = models.AutoField(primary_key=True, editable=False, auto_created=True)
    data_ini = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    cargo = models.IntegerField(null=False, blank=-False) #1(Mot) 2(Ajud)
    fator = models.IntegerField(null=False, blank=-False)
    val_caixaria = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    val_entrega = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    tipo_recarga = models.IntegerField(null=False, blank=-False) #1(Fixa) 2(Caixa) 3(NA)
    val_recarga = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'op_conecta_param_rv_rota'


class Registro_2art_Rota(models.Model):
    cod_reg_2art_rota = models.IntegerField(primary_key=True)
    data = models.DateField(null=True)
    entrega = models.CharField(max_length=20, null=True)
    cargaatual = models.CharField(max_length=20, null=True)
    frota = models.CharField(max_length=20, null=True)
    placa = models.CharField(max_length=10, null=True)
    mapa = models.CharField(max_length=10, null=True)
    entregas = models.CharField(max_length=5, null=True)
    cxcarreg = models.CharField(max_length=10, null=True)
    cxentreg = models.CharField(max_length=10, null=True)
    hrsai = models.CharField(max_length=25, null=True)
    hrentr = models.CharField(max_length=25, null=True)
    qtentregascarregrv = models.CharField(max_length=5, null=True)
    qtentregasentregrv = models.CharField(max_length=5, null=True)
    indicedeventregasrv = models.CharField(max_length=15, null=True)
    fator = models.CharField(max_length=5, null=True)
    matricula_colab = models.CharField(max_length=10, null=True)
    cpf_colab = models.CharField(max_length=15, null=True)
    funcao = models.IntegerField(null=True, blank=True) #1(Motorista) 2(Ajud 1) 3(Ajud 2)
    alteracao = models.IntegerField(null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    cod_param_rv_rota = models.ForeignKey(Param_RV_Rota, models.DO_NOTHING, db_column='cod_param_rv_rota')
    class Meta():
        managed = True
        db_table = 'op_conecta_2art_rota'

