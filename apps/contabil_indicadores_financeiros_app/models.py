from django.db import models

from apps.usuario_app.models import Usuario

class Estrutura_Contas(models.Model):
    cod_estrutura_conta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    nome_estrutura = models.CharField(max_length=70, blank=False, null=False)
    nivel = models.IntegerField(blank=False, null=False)
    eh_ultimo_nivel = models.DateTimeField(blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', blank=True,
                                         null=True)
    cod_conta = models.DateTimeField(blank=True, null=True)
    data_criacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_contabil_estrutura_contas'

class Conta(models.Model):
    cod_conta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    nome_conta = models.CharField(max_length=70, blank=False, null=False)
    id_conta_benner = models.IntegerField(blank=False, null=False)
    cod_estrutura_conta = models.DateTimeField(blank=True, null=True)
    data_atribuicao = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_contabil_contas'
