from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado

class Gabarito_GSO(models.Model):
    cod_gabarito_onibus_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    placa_onibus = models.CharField(max_length=10, blank=False, null=False)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=False,
                                         null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_gso'
