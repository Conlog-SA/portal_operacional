from django.db import models

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado
from apps.safety_gab_op_emp_app.models import Empilhadeira


class Check_Empilhadeira(models.Model):
    cod_empilhadeira_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_empilhadeira = models.ForeignKey(Empilhadeira, models.DO_NOTHING, db_column='cod_empilhadeira', blank=True,
                                         null=True)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_check_empilhadeira'

