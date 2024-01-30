from django.db import models

from apps.safety_layout_checklist_app.models import Layout_Check, Item_Check

class Colaborador(models.Model):
    cod_colaborador = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    matricula_colaborador = models.IntegerField(blank=False, null=False)
    nome_colaborador = models.CharField(max_length=100, blank=False, null=False)
    cod_empresa = models.IntegerField(blank=False, null=False)
    desc_cargo = models.CharField(max_length=80, blank=False, null=False)
    cnh = models.CharField(max_length=20, blank=False, null=False)
    validade_cnh = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_colaboradores'

class Check_Aplicado(models.Model):
    cod_checks_aplicados = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_filial = models.IntegerField(blank=False, null=False)
    cod_colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='cod_colaborador', blank=True,
                                         null=True)
    comentarios = models.CharField(max_length=300, blank=False, null=False)
    data_registro = models.DateTimeField(blank=True, null=True)
    cod_layout_check = models.ForeignKey(Layout_Check, models.DO_NOTHING, db_column='cod_layout_check', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_checks_aplicados'

class Item_Check_Aplicados(models.Model):
    cod_item_ap = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_item_check = models.ForeignKey(Item_Check, models.DO_NOTHING, db_column='cod_item_check', blank=True,
                                         null=True)
    resp_item = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_safe_itens_checks_aplicados'

class Item_Fotos_Texto_Check_Aplicado(models.Model):
    cod_item_fotos_texto_itens_checks_aplicados = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    comentario = models.CharField(max_length=40, blank=False, null=False)
    caminho_imagem = models.CharField(max_length=80, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_itens_fotos_texto_checks_aplicados'