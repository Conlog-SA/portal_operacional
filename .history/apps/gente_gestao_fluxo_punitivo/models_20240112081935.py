from django.db import models
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import Filial

class Gente_Gestao_Motivo_Juridico(models.Model):
    cod_mot_juridico = models.AutoField(primary_key=True, editable=False, auto_created=True)
    desc_motivo_juridico = models.CharField(max_length=70, null=False, blank=False)
    class Meta():
        managed=True
        db_table='ger_gente_gestao_fluxo_punitivo_motivo_juridico'#op_geg_fluxo_punitivo_motivo_juridico'


class Gente_Gestao_Motivo_Especifico(models.Model):
    cod_mot_especifico = models.AutoField(primary_key=True, editable=False, auto_created=True)
    desc_motivo_especifico = models.CharField(max_length=70, null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_gente_gestao_fluxo_punitivo_motivo_especifico'#'op_geg_fluxo_punitivo_motivo_especifico'

class Gente_Gestao_Punicao(models.Model):
    cod_punicao = models.AutoField(primary_key=True, editable=False, auto_created=True)
    nome_colab = models.CharField(max_length=150, null=False, blank=False)
    matricula_colab = models.IntegerField(null=False, blank=False)
    data_admissao = models.DateField(null=False, blank=False)
    cpf_colab = models.BigIntegerField(null=False, blank=False)
    cod_cargo_colab = models.IntegerField(null=False, blank=False)
    desc_cargo_colab = models.CharField(max_length=80, null=False, blank=False)
    situacao_colab = models.CharField(max_length=30, null=False, blank=False)
    #! Tipos de pensalidade : N(Notificação), AV(Advertência Verbal), AE(Advertência Escrita), S(Suspensão)
    penalidade = models.CharField(max_length=2, null=False, blank=False)
    data_ocorrencia = models.DateField(null=False, blank=False)
    data_registro = models.DateField(auto_now_add=True)
    desc_motivo = models.CharField(max_length=300, null=False, blank=False)
    ativo = models.CharField(max_length=1, null=False, blank=False, default='S')
    obs_punicao = models.CharField(max_length=300, null=True, blank=True)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', null=False, blank=False)
    cod_mot_juridico = models.ForeignKey(Gente_Gestao_Motivo_Juridico, models.DO_NOTHING, db_column='cod_mot_juridico',
                                         null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_mot_especifico = models.ForeignKey(Gente_Gestao_Motivo_Especifico, models.DO_NOTHING,
                                           db_column='cod_mot_especifico', null=True, blank=True)
    class Meta():
        managed = True
        db_table='ger_gente_gestao_fluxo_punitivo_punicao'#op_geg_fluxo_punitivo_lancamentos'

class Gente_Gestao_Dias_Suspensao(models.Model):
    cod_dias_suspensao = models.AutoField(primary_key=True, editable=False, auto_created=True)
    inicio_suspensao = models.DateField(null=False, blank=False)
    fim_suspensao = models.DateField(null=False, blank=False)
    cod_punicao = models.ForeignKey(Gente_Gestao_Punicao, models.DO_NOTHING, db_column='cod_punicao',
                                    null=False, blank=False)
    class Meta():
        managed = True
        db_table='ger_gente_gestao_fluxo_punitivo_dias_suspensao'#op_geg_fluxo_punitivo_dias_suspensao'


class Gente_Gestao_Desativacao(models.Model):
    cod_desativacao = models.AutoField(primary_key=True, editable=False, auto_created=True)
    motivo_desativacao = models.CharField(null=True, blank=True)
    data_desativacao = models.DateTimeField(auto_now_add=True)

    class Meta():
        managed = True
        db_table = 'ger_gente_gestao_fluxo_punitivo_desativacao_punicao'