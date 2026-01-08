from django.db import models

class Empresa(models.Model):
    cod_empresa = models.IntegerField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_benner = models.IntegerField(null=True, blank=True, default=0)
    handle_gn_proj_benner = models.IntegerField(null=True, blank=True, default=0)
    estrutura_benner = models.CharField(max_length=1, null=True, blank=True, default=0)
    cod_senior = models.IntegerField(null=True, blank=True, default=0)
    desc_empresa = models.CharField(max_length=70)
    data_inativado = models.DateField(null=True)
    class Meta():
        managed=True
        db_table='ger_empresa'


class Operacao(models.Model):
    cod_operacao = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_operacao = models.CharField(max_length=50)
    handle_gn_proj_benner = models.IntegerField(null=True, blank=True, default=0)
    estrutura_benner = models.CharField(max_length=4, null=True, blank=True, default=0)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING,db_column='cod_empresa',null=True)
    class Meta():
        managed = True
        db_table = 'ger_operacoes'

class Filial(models.Model):
    cod_filial = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_operacao = models.ForeignKey(Operacao, models.DO_NOTHING, db_column='cod_operacao', null=True)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING,db_column='cod_empresa',null=True)
    cnpj_filial = models.CharField(max_length=14,null=True)
    desc_filial = models.CharField(max_length=70,null=True)
    handle_benner = models.IntegerField(null=True)
    estrutura_benner = models.CharField(max_length=7, null=True, blank=True, default=0)
    unidade_abrev = models.CharField(max_length=3, null=True)
    cod_filial_senior = models.IntegerField(null=True)
    cod_reduzido = models.IntegerField(null=True)
    cod_promax = models.IntegerField(null=True)
    cod_filial_tracking = models.IntegerField(null=True)
    ativo = models.IntegerField(default=1)
    regiao = models.CharField(max_length=30, null=True, blank=True)
    tem_calculo_rv = models.IntegerField(null=True, blank=True, default=0)
    handle_gn_proj_benner = models.IntegerField(null=True, blank=True, default=0)
    usuario_freightech = models.CharField(max_length=50, null=False)
    senha_freightech = models.CharField(max_length=50, null=False)
    class Meta:
        managed = True
        db_table = 'ger_filial'


class Atividade(models.Model):
    cod_atividade = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc1_atividade = models.CharField(max_length=30)
    desc2_atividade = models.CharField(max_length=15)
    class Meta():
        managed = True
        db_table = 'ger_atividades_projeto'


class Projeto(models.Model):
    cod_projeto = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_reduzido_benner = models.IntegerField(null=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', blank=True, null=True)
    cod_atividade = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='cod_atividade', blank=True, null=True)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='cod_empresa', null=True)
    desc_proj = models.CharField(max_length=70, null=True)
    cod_local_senior = models.CharField(max_length=50, null=True)
    handle_benner = models.IntegerField(default=None)
    cod_senior = models.IntegerField(default=None)
    cod_serial_pag_terc = models.CharField(max_length=3, null=True)
    ultimo_num_pagamento = models.IntegerField(null=True)
    neg_aloc = models.IntegerField(null=True)
    data_inativado = models.DateField(null=True)
    data_inicio = models.DateField(null=True)
    integra_frota = models.CharField(max_length=1,null=True)
    ctrl_cluster_dre = models.CharField(max_length=1,null=True)
    class Meta:
        managed = True
        db_table = 'ger_projetos'



class OP_Estados(models.Model):
    cod_estado = models.AutoField(primary_key=True, editable=True, blank=False, auto_created=True)
    estado = models.CharField(max_length=30)
    class Meta():
        managed = True
        db_table = 'ger_estados'


