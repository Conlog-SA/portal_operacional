from django.db import models

# Create your models here.
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import  Filial


class Relacao_Filial_Comprador(models.Model):
    cod_rel_filial_comprador = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_ini = models.DateField(null=False, blank=False)
    data_fim = models.DateField(null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    class Meta():
        managed=True
        db_table='ger_suprimentos_relacao_filial_comprador'#op_suprimentos_relacao_filial_comprador'