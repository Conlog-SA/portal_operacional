from django.db import models
from apps.usuario_app.models import Usuario

# Create your models here.


class Conexao(models.Model):
    cod_conexao = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    erp = models.CharField(max_length=25, blank=False, null=False)
    string_conexao = models.CharField(max_length=500, blank=False, null=False)
    ativo = models.IntegerField(blank=False, null=False) #0 -- Desativo 1-- Ativo

    class Meta:
        managed = True
        db_table = 'op_ti_gc_conexao'

class Script(models.Model):
    cod_script = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc = models.CharField(max_length=50, blank=False, null=False)
    script = models.TextField(max_length=700, blank=False, null=False)
    obs = models.CharField(max_length=500, blank=False, null=False)
    data_criacao = models.DateField(null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    data_ultima_alteracao = models.DateField(null=False, blank=False)
    cod_conexao = models.ForeignKey(Conexao, models.DO_NOTHING, db_column='cod_conexao', null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'op_ti_gc_scripts'

class Parametro(models.Model):
    cod_param = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc = models.CharField(max_length=35, blank=False, null=False)
    tipo = models.IntegerField(blank=False, null=False) #1-- Date 2-- Int 3--String
    cod_script = models.ForeignKey(Script, models.DO_NOTHING, db_column='cod_script', blank=False,
                                    null=False)

    class Meta:
        managed = True
        db_table = 'op_ti_gc_parametros'

class Liberacao(models.Model):
    cod_liberacao = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_script = models.ForeignKey(Script, models.DO_NOTHING, db_column='cod_script', blank=False,
                                    null=False)

    class Meta:
        managed = True
        db_table = 'op_ti_gc_liberacoes'

