import os

from django.db import models

from apps.safety_checks_aplicados_app.models import Check_Aplicado
from apps.safety_layout_checklist_app.models import Itens_Componentes


class Registro_Ocorrencia(models.Model):
    cod_reg_ocorrencia = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_check_aplicado = models.ForeignKey(Check_Aplicado, models.DO_NOTHING, db_column='cod_check_aplicado',
                                           blank=True,
                                           null=True)
    data_ocorrencia = models.DateTimeField(blank=False, null=False)
    cod_negocio = models.IntegerField(blank=True, null=True)
    cod_tipo = models.IntegerField(blank=True, null=True)
    nome_empresa_envolvida = models.CharField(max_length=200, blank=False, null=False)
    turno = models.CharField(max_length=1, blank=False, null=False)
    cod_nexo = models.IntegerField(blank=True, null=True)
    cod_classificacao = models.IntegerField(blank=True, null=True)
    cod_risco_real = models.IntegerField(blank=True, null=True)
    nome_envolvidos = models.CharField(max_length=500, blank=False, null=False)
    funcao_envolvidos = models.CharField(max_length=500, blank=False, null=False)
    cod_local_ocorrencia = models.ForeignKey(Itens_Componentes, models.DO_NOTHING, db_column='cod_local_ocorrencia',
                                             related_name='cod_local_ocorrencia', blank=True)
    area_detalhada = models.CharField(max_length=200, blank=False, null=False)
    cod_atividade = models.ForeignKey(Itens_Componentes, models.DO_NOTHING, db_column='cod_atividade',
                                      related_name='cod_atividade', blank=True)
    cod_natrueza = models.ForeignKey(Itens_Componentes, models.DO_NOTHING, db_column='cod_natrueza',
                                      related_name='cod_natrueza', blank=True)
    desc_parte = models.CharField(max_length=200, blank=False, null=False)
    desc_dano = models.CharField(max_length=200, blank=False, null=False)
    ativo_envolvido = models.CharField(max_length=200, blank=False, null=False)
    causa = models.CharField(max_length=200, blank=False, null=False)
    breve_relato = models.CharField(max_length=200, blank=False, null=False)
    'E(Editado), C(Completo)'
    status = models.CharField(max_length=1, default='E')

    class Meta:
        managed=True
        db_table="op_safe_registro_ocorrencia_check"





