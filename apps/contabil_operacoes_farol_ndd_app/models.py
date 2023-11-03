from django.db import models

from apps.usuario_app.models import Usuario


class Notas_Tratadas(models.Model):
    cod_nota_tratada = models.AutoField(primary_key=True, editable=False, auto_created=True)
    handle_empresa = models.IntegerField(null=False, blank=False)
    nome_empresa = models.CharField(max_length=50, null=False, blank=False)
    handle_filial = models.IntegerField(null=False, blank=-False)
    nome_filial = models.CharField(max_length=70, null=False, blank=False)
    numero_nota = models.IntegerField(null=False, blank=False)
    serie = models.IntegerField(null=True, blank=True)
    chave_nota = models.CharField(max_length=44, null=False, blank=False)
    natureza = models.CharField(max_length=60, null=True, blank=True)
    emissao = models.DateField(null=False, blank=False)
    doc_fornec = models.CharField(max_length=19, null=False, blank=False)
    nome_fornec = models.CharField(max_length=60, null=True, blank=False)
    justificativa = models.CharField(max_length=300, null=False, blank=False)
    data_registro = models.DateField(auto_now_add=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'op_contabil_notas_tratadas'


class Excecoes_Natureza_Operacao(models.Model):
    cod_excecao_operacao = models.AutoField(primary_key=True, editable=False, auto_created=True)
    desc_operacao = models.CharField(max_length=60, null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'op_contabil_excecoes_natureza_operacao'
