from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado


# Create your models here.
class Blitz_Trajeto_Bicicleta(models.Model):
    cod_blitz_trajeto_bicicleta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=False,
                                         null=False)
    '''1(Funcionario COnlog/Deep)/ 2(Funcionario Ambev/ 3(Freteiro)/ 4(Terceiro)'''
    situacao_colaborador = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'op_safe_blitz_trajeto_bicicleta'