from django.db import models

class Respostas_Entrevista_Desligamento(models.Model):
    matricula = models.CharField(max_length=15, blank=False, null=False)
    data_emissao_link = models.DateTimeField(null=False, blank=False)
    data_preenchimento = models.DateTimeField(null=False, blank=False)
    respostas_formulario = models.TextField(null=True)
    data_anotacoes_especialista = models.DateTimeField(null=False, blank=False)
    anotacoes_especialista = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos_respostas_entrevista'

class Desligamento(models.Model):
    matricula = models.CharField(max_length=15, blank=False, null=False)
    nome = models.CharField(max_length=12, blank=False, null=False)
    cod_unidade = models.IntegerField(blank=False, null=False)
    unidade = models.CharField(max_length=100, blank=False, null=False)
    data_admissao = models.DateTimeField(null=False, blank=False)
    data_desligamento = models.DateTimeField(null=False, blank=False)
    cargo = models.CharField(max_length=100, blank=False, null=False)
    contato_telefone = models.CharField(max_length=30, blank=False, null=False)
    contato_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos'