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
    data_comp = models.DateField(null=False, blank=False)
    handle_lanc = models.IntegerField(null=False, blank=False)
    handle_lanc_cc = models.IntegerField(null=False, blank=False)
    handle_fn_doc = models.IntegerField(null=False, blank=False)
    placa = models.CharField(max_length=10, null=False, blank=False)
    handle_projeto = models.IntegerField(null=False, blank=False)
    desc_projeto = models.CharField(max_length=80, null=False, blank=False)
    desc_conta = models.CharField(max_length=60, null=False, blank=False)
    desc_tipo_conta = models.CharField(max_length=60, null=False, blank=False)
    doc_contabil = models.CharField(max_length=30, null=True, blank=True)
    data_lancamento = models.DateField(null=False, blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    historico = models.CharField(max_length=500, null=True, blank=True)
    nome_fornecedor = models.CharField(max_length=80, null=True, blank=True)
    cod_item_cluster = models.ForeignKey(Item_Cluster, models.DO_NOTHING, null=True, blank=True,
                                         db_column='cod_item_cluster')
    class Meta:
        managed = True
        db_table = 'op_frota_custos_razao_cluster'


class Os_Razao_Frota(models.Model):
    cod_os_razao_frota = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_lanc_cc = models.IntegerField(null=False, blank=False)
    handle_os = models.IntegerField(null=False, blank=False)
    cod_os = models.CharField(max_length=20, null=False, blank=False)
    desc_os = models.CharField(max_length=80, null=False, blank=False)
    handle_tipo_os = models.IntegerField(null=False, blank=False)
    desc_tipo_os = models.CharField(max_length=50, null=False, blank=False)
    obs_os = models.CharField(max_length=500, null=False, blank=False)
    handle_prod = models.IntegerField(null=False, blank=False)
    desc_prod = models.CharField(max_length=80, null=False, blank=False)
    qtd_prod = models.IntegerField(null=False, blank=False)
    desc_conj = models.CharField(max_length=80, null=False, blank=False)
    un_prod = models.CharField(max_length=20, null=False, blank=False)
    eh_cluster = models.IntegerField(null=True, blank=True, default=0)
    cod_razao_frota = models.ForeignKey(Razao_Frota, models.DO_NOTHING, null=True, blank=True,
                                        db_column='cod_razao_frota')
    class Meta:
        managed = True
        db_table = 'op_frota_custos_os_razao_cluster'




