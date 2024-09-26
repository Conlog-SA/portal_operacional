from django.db import models

from apps.estrut_org_app.models import Projeto
from apps.usuario_app.models import Usuario

class Operadora_Plano(models.Model):
    cod_operadora_plano = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_operadora_plano = models.CharField(max_length=80, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_rateio_unimed_operadoras_plano'

class Plano_Saude(models.Model):
    cod_plano_saude = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    filial = models.CharField(max_length=80, blank=False, null=False)
    especificacao = models.CharField(max_length=80, blank=True, null=True)
    percentual_empresa_titular = models.IntegerField(blank=True, null=True)
    percentual_empresa_dependente = models.IntegerField(blank=True, null=True)
    percentual_empresa_copay = models.IntegerField(blank=True, null=True)
    operadora_plano = models.ForeignKey(Operadora_Plano, models.DO_NOTHING, db_column='operadora_plano', blank=False,
                      null=False)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_rateio_unimed_planos'

class Arquivo_Despesas(models.Model):
    cod_arq_despesa = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    nome_arq_imp = models.CharField(max_length=100, blank=False, null=False)
    nome_arq_original = models.CharField(max_length=100, blank=False, null=False)
    competencia_informada = models.DateField(blank=True, null=True)
    qtd_registros = models.IntegerField(blank=False, null=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    status_arquivo = models.IntegerField(blank=False, null=False)
    data_desativacao = models.DateTimeField(null=False, blank=False)
    cod_usu_desativacao = models.IntegerField(blank=False, null=False)
    cod_plano_saude = models.ForeignKey(Plano_Saude, models.DO_NOTHING, db_column='cod_plano_saude', blank=False,
                                    null=False)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_rateio_unimed_arquivos'

class Despesa_Unimed(models.Model):
    cod_despesa_unimed = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    competencia = models.CharField(max_length=50, blank=False, null=False)
    nome_beneficiario = models.CharField(max_length=100, blank=False, null=False)
    cpf_beneficiario = models.CharField(max_length=20, blank=False, null=False)
    tipo_depencencia = models.CharField(max_length=40, blank=False, null=False)
    nome_titular = models.CharField(max_length=80, blank=True, null=True)
    cpf_titular = models.CharField(max_length=20, blank=True, null=True)
    desc_despesa = models.CharField(max_length=40, blank=True, null=True)
    valor = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    matricula_titular = models.IntegerField(blank=True, null=True)
    nome_titular_senior = models.CharField(max_length=100, blank=False, null=False)
   # nome_beneficiario_senior = models.CharField(max_length=100, blank=False, null=False)
    cod_projeto_senior = models.CharField(max_length=30, blank=False, null=False)
    desc_projeto_senior = models.TextField(max_length=255, blank=True, null=True)
    cod_filial_senior = models.IntegerField(blank=True, null=True)
    desc_filial_senior = models.TextField(max_length=50, blank=True, null=True)
    cod_empresa_senior = models.IntegerField(blank=True, null=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', blank=False,
               null=False)
    cod_arq_despesa = models.ForeignKey(Arquivo_Despesas, models.DO_NOTHING, db_column='cod_arq_despesa', blank=False,
                                    null=False)
    percentual_empresa = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_rateio_unimed_despesas'

