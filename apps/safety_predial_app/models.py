from django.db import models

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado


class Check_Predial(models.Model):
    cod_predial_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_area = models.IntegerField(blank=False, null=False)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_predial'