from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado

class Gabarito_GSDPQ(models.Model):
    cod_gabarito_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    placa_caminhao = models.CharField(max_length=20, blank=False, null=False)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_gsdpq'
