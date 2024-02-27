from django.db import models

class Modelo_Emp(models.Model):
    cod_modelo_emp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_emp = models.CharField(max_length=40, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_modelo_emp'

class Tipo_Operacao_Emp(models.Model):
    cod_tipo_operacao_emp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_tipo_operacao_desc = models.CharField(max_length=70, blank=False, null=False)
    modelo_emp = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_tipo_operacao'

class Gabarito_Operacional_Emp(models.Model):
    cod_item_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    tipo_operador = models.IntegerField(blank=False, null=False)
    cod_modelo_emp = models.ForeignKey(Modelo_Emp, models.DO_NOTHING, db_column='cod_modelo_emp', blank=True,
                                         null=True)
    cod_tipo_operacao_emp = models.ForeignKey(Tipo_Operacao_Emp, models.DO_NOTHING, db_column='cod_tipo_operacao_emp', blank=True,
                                         null=True)
    cod_avaliador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_gab_op_emp'