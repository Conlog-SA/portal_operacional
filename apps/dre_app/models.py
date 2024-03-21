from django.db import models

from apps.usuario_app.models import Usuario


class Layout_Dre(models.Model):
    cod_lay_dre = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_lay = models.CharField(max_length=80, blank=False, null=False)
    ini_vigencia = models.DateField(null=False, blank=False)
    fim_vigencia = models.DateField(null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', blank=False, null=False)
    class Meta:
        managed=True
        db_table = 'op_dre_layout'

class Estrutura_Dre(models.Model):
    cod_str_dre = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc = models.CharField(max_length=80, blank=False, null=False)
    cod_nivel = models.IntegerField(null=False, blank=False)
    cod_str_dre_pai = models.IntegerField(null=False, blank=False, default=0)
    eh_ultimo_nivel = models.CharField(max_length=1, blank=False, default=False)
    ini_vigencia = models.DateField(null=False, blank=False)
    fim_vigencia = models.DateField(null=True, blank=True)
    cod_lay_dre = models.ForeignKey(Layout_Dre, models.DO_NOTHING, db_column='cod_lay_dre', blank=False, null=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'op_dre_estrutura'


class Dre_Contas_Benner(models.Model):
    cod_dre_conta_benner = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_conta = models.IntegerField(null=False, blank=False)
    desc_conta = models.CharField(max_length=80, null=False, blank=False)
    cod_str_dre = models.ForeignKey(Estrutura_Dre, models.DO_NOTHING, db_column='cod_str_dre', blank=False, null=False)

