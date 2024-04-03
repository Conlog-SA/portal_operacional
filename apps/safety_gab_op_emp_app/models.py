from django.db import models

from apps.estrut_org_app.models import Filial


class Empilhadeira(models.Model):
    cod_emp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    placa = models.CharField(max_length=40, blank=False, null=False)
    desc_placa = models.CharField(max_length=100, blank=False, null=False)
    ano_placa = models.CharField(max_length=40, blank=False, null=False)
    modelo_placa = models.CharField(max_length=40, blank=False, null=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', blank=False,
                                         null=False)


    class Meta:
        managed = True
        db_table = 'op_safe_empilhadeiras'

class Gabarito_Operacional_Emp(models.Model):
    cod_item_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    tipo_operador = models.IntegerField(blank=False, null=False)
    cod_empilhadeira = models.ForeignKey(Empilhadeira, models.DO_NOTHING, db_column='cod_empilhadeira', blank=True,
                                         null=True)
    cod_avaliador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_gab_op_emp'

