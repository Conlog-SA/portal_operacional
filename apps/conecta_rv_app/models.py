from django.db import models

from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario

class Param_Bonus_Devolucao_RV(models.Model):
    cod_param_bonus_dev_rv = models.AutoField(primary_key=True, editable=False, auto_created=True)
    data_ini = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    cargo = models.IntegerField(null=False, blank=False)  # 1(Mot) 2(Ajud)
    perc_meta = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    val_bonus_dev = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'op_conecta_param_bonus_dev_rv'

class Verbas_Senior_RV(models.Model):
    cod_verba_senior_rv = models.AutoField(primary_key=True, editable=False, auto_created=True)
    data_ini = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    tipo_verba = models.IntegerField(null=True, blank=True) #1(Rota) 2(AS) 3(Vans) 4(Recarga) 5(Adicional) 6(Bonus)
    cod_verba = models.CharField(max_length=3, null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'op_conecta_verbas_senior_rv'
