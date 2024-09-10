from django.db import models

# Create your models here.
class Item_Cluster(models.Model):
    cod_item_cluster = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_item_cluster = models.CharField(max_length=80, null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_frota_custos_itens_cluster'

class Razao_Frota(models.Model):
    cod_razao_frota = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_lanc = models.IntegerField(null=False, blank=False)
    placa = models.CharField(max_length=10, null=False, blank=False)
    handle_projeto = models.IntegerField(null=False, blank=False)
    desc_projeto = models.CharField(max_length=80, null=False, blank=False)
    desc_tipo_conta = models.CharField(max_length=60, null=False, blank=False)
    doc_contabil = models.CharField(max_length=30, null=True, blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    historico = models.CharField(max_length=500, null=True, blank=True)
    nome_fornecedor = models.CharField(max_length=80, null=True, blank=True)
    codigo_os = models.CharField(max_length=60, null=True, blank=True)
    desc_os = models.CharField(max_length=500, null=True, blank=True)
    desc_tipo_os = models.CharField(max_length=80, null=True, blank=True)
    obs_os = models.CharField(max_length=500, null=True, blank=True)
    itens_os = models.CharField(max_length=500, null=True, blank=True)
    cod_item_cluster = models.ForeignKey(Item_Cluster, models.DO_NOTHING, null=True, blank=True,
                                         db_column='cod_item_cluster')
    class Meta:
        managed = True
        db_table = 'op_frota_custos_razao_cluster'
