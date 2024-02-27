from django.db import models

from django.db import models


class Tipo_Relato(models.Model):
    cod_tipo_relato = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_tipo_relato = models.CharField(max_length=70, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_tipo_relatos'

class Relato(models.Model):
    cod_relato_check = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_tipo_relato = models.ForeignKey(Tipo_Relato, models.DO_NOTHING, db_column='cod_tipo_relato', blank=True,
                                         null=True)
    situacao_envolvido = models.IntegerField(blank=False, null=False)
    nome_relatado = models.CharField(max_length=70, blank=True, null=True)
    local_relato = models.CharField(max_length=70, blank=False, null=False)
    atividade_relato = models.CharField(max_length=70, blank=False, null=False)
    descricao_relato = models.CharField(max_length=70, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_relatos'
