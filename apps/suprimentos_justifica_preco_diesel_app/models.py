from django.db import models

from apps.usuario_app.models import Usuario


class Motivo_Just_Preco_Diesel(models.Model):
    cod_motivo_just_preco_diesel = models.AutoField(primary_key=True, editable=False, auto_created=True)
    desc_motivo_just_preco_diesel = models.CharField(max_length=30)
    class Meta():
        managed=True
        db_table='op_suprimentos_motivo_just_preco_diesel'

class Justificativa_Preco_Diesel(models.Model):
    cod_just_preco_diesel = models.AutoField(primary_key=True, editable=False, auto_created=True)
    handle_itens_compra = models.IntegerField(null=False, blank=False)
    num_compra = models.CharField(max_length=20, null=False, blank=False)
    data_compra = models.DateField()
    val_unit_compra = models.DecimalField(max_digits=8, decimal_places=2)
    val_compra_ant = models.DecimalField(max_digits=8, decimal_places=2)
    handle_filial = models.IntegerField(null=False, blank=False)
    nome_filial = models.CharField(max_length=50)
    data_justificativa = models.DateField(auto_now_add=True)
    desc_justificativa = models.CharField(max_length=300)
    cod_motivo_just_preco_diesel = models.ForeignKey(Motivo_Just_Preco_Diesel, models.DO_NOTHING,
                                                     db_column='cod_motivo_just_preco_diesel', null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed=True
        db_table='op_suprimentos_justificativa_preco_diesel'

