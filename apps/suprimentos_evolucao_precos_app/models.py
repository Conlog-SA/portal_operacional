from django.db import models
from django.views import View

from apps.usuario_app.models import Usuario


class Compra_Auditada(models.Model):
    cod_compra_aud = models.AutoField(primary_key=True, editable=False, auto_created=True)
    handle_filial_compra = models.IntegerField()
    handle_itens_compra = models.IntegerField()
    handle_produto = models.IntegerField()
    val_unit = models.DecimalField(max_digits=8, decimal_places=2)
    qtd_item = models.IntegerField()
    data_aud = models.DateField(auto_now_add=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed=True
        db_table = 'op_suprimentos_compras_aud'



class Justificativa_Compra(models.Model):
    cod_justificativa_compra = models.AutoField(primary_key=True, editable=False, auto_created=True)
    justificativa = models.CharField(max_length=300, null=True, blank=True)
    eh_ativa = models.CharField(max_length=1, null=False, blank=False, default='S')
    data_cad = models.DateField(auto_now_add=True)
    handle_itens_compra = models.IntegerField()
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed=True
        db_table = 'op_suprimentos_evolucao_preco_justificativas'