from django.db import models

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado


class Check_Pci(models.Model):
    cod_pci_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    item = models.IntegerField(blank=False, null=False)
    local = models.CharField(max_length=300, null=True, blank=True, default='')
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_pci'