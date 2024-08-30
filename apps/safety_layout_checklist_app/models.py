from django.db import models

from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario

class Layout_Check(models.Model):
    cod_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_check = models.CharField(max_length=70, blank=False, null=False)
    versao = models.IntegerField(blank=False, null=False)
    data_inclusao = models.DateTimeField(blank=True, null=True)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_desativacao = models.DateTimeField(blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', blank=True,
                                         null=True)
    periodicidade = models.CharField(max_length=1, blank=True, null=True)
    medida_periodicidade = models.IntegerField(blank=False, null=False)
    tipo_check = models.CharField(max_length=30, blank=False, null=False)
    ativo=models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'op_safe_layout_check'

class Item_Check(models.Model):
    cod_item_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_check = models.CharField(max_length=300, blank=False, null=False)
    tipo_resposta = models.IntegerField(blank=True, null=True)
    data_inclusao = models.DateTimeField(blank=True, null=True)
    cod_usuario = models.IntegerField(blank=False, null=False)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_desativacao = models.DateTimeField(blank=True, null=True)
    campo_obs_img = models.IntegerField(blank=False, null=False)
    #campo_img = models.IntegerField(blank=False, null=False)
    obrigatorio = models.IntegerField(blank=False, null=False)
    ordem_item = models.IntegerField(blank=False, null=False)
    tipo_item = models.IntegerField(blank=False, null=False)
    cod_check = models.ForeignKey(Layout_Check, models.DO_NOTHING, db_column='cod_check', blank=True,
                                         null=True)
    class Meta:
        managed = True
        db_table = 'op_safe_item_check'

class Libera_Filial_Check(models.Model):
    cod_libera_filial = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_check = models.ForeignKey(Layout_Check, models.DO_NOTHING, db_column='cod_check', blank=True,
                                         null=True)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', blank=True,
                                         null=True)
    data_desativacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_check_libera_filial'

class Itens_Componentes(models.Model):
    cod_componente = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    tipo_check = models.IntegerField(blank=False, null=False)
    campo_check = models.IntegerField(blank=False, null=False)
    cod_pai = models.IntegerField(blank=False, null=False)
    desc_componente = models.CharField(max_length=80, blank=False, null=False)
    cod_empresa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_itens_componentes_forms'
