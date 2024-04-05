from django.db import models

class Colaborador(models.Model):
    cod_colaborador = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    matricula_colaborador = models.IntegerField(blank=True, null=True)
    nome_colaborador = models.CharField(max_length=100, blank=False, null=False)
    cod_filial = models.IntegerField(blank=False, null=False)
    desc_cargo = models.CharField(max_length=80, blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    validade_cnh = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    perfil_usu = models.CharField(max_length=1, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'op_safe_colaboradores'
