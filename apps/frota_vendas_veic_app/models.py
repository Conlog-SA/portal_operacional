from django.db import models

# Create your models here.

class Tabela_Preco_Veic(models.Model):
    cod_tab_precos = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_tabela = models.CharField(max_length=80, blank=False, null=False)
    site_inst = models.CharField(max_length=150, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'op_frota_tab_preco_veic'


class Tipo_Veic_Tab_Precos(models.Model):
    cod_tipo_veic_tab_precos = models.IntegerField(primary_key=True, blank=False, null=False)
    desc_tipo_veic = models.CharField(max_length=15, blank=False, null=False)
    id_tipo_veic_tab = models.IntegerField(blank=True, null=True)
    cod_tab_precos = models.ForeignKey(Tabela_Preco_Veic, models.DO_NOTHING, db_column='cod_tab_precos', null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'op_frota_tipo_veic_tab_precos'


class Marca_Tab_Precos(models.Model):
    cod_marca_tab_precos = models.IntegerField(primary_key=True, blank=False, null=False)
    desc_marca = models.CharField(max_length=15, blank=False, null=False)
    cod_tipo_veic_tab_precos = models.ForeignKey(Tipo_Veic_Tab_Precos, models.DO_NOTHING, db_column='cod_tipo_veic_tab_precos')
    class Meta:
        managed = True
        db_table = 'op_frota_marca_tab_precos'


class Modelo_Tab_Precos(models.Model):
    cod_modelo_tab_precos = models.IntegerField(primary_key=True, blank=False, null=False)
    desc_modelo = models.CharField(max_length=300, blank=False, null=False)
    cod_marca_tab_precos = models.ForeignKey(Marca_Tab_Precos, models.DO_NOTHING, db_column='cod_marca_tab_precos')
    class Meta:
        managed = True
        db_table = 'op_frota_modelo_tab_precos'


class Veiculo_Venda(models.Model):
    cod_veic = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_veic = models.IntegerField(blank=False, null=False)
    placa = models.CharField(max_length=10, blank=False, null=False)
    eixo = models.IntegerField(blank=True, null=True)
    tipo_veic = models.CharField(max_length=80, blank=False, null=False)
    renavam = models.CharField(max_length=15, blank=True, null=True)
    uf_compra = models.CharField(max_length=2, blank=True, null=True)
    marca = models.CharField(max_length=15, blank=False, null=False)
    modelo = models.CharField(max_length=25, blank=False, null=False)
    ano = models.IntegerField(blank=False, null=False)
    nome_filial  =models.CharField(max_length=100, blank=True, null=True)
    status_ativo_benner = models.CharField(max_length=1, blank=True, null=True)
    num_nf_venda = models.CharField(max_length=15, blank=True, null=True)
    data_venda = models.DateField(blank=True, null=True)
    val_venda = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    nome_cliente = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'op_frota_veic_venda'


class Veiculo_Venda_Tab_Precos(models.Model):
    cod_veic_venda_tab = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    codigo_veic_tab = models.CharField(max_length=10, blank=True, null=True)
    competencia = models.DateField(null=True, blank=True)
    val_comp = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    ano_veic_tab = models.IntegerField(blank=False, null=False)
    cod_veic = models.ForeignKey(Veiculo_Venda, models.DO_NOTHING, db_column='cod_veic')
    cod_modelo_tab_precos = models.ForeignKey(Modelo_Tab_Precos, models.DO_NOTHING, db_column='cod_modelo_tab_precos',
                                            null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'op_frota_veic_venda_tab_precos'







