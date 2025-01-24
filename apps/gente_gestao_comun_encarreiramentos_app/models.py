from django.db import models

class Encarreiramento(models.Model):
    cod_encarreiramento = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_empresa = models.IntegerField(blank=False, null=False)
    cod_unidade = models.IntegerField(blank=False, null=False)
    matricula = models.CharField(max_length=12, blank=False, null=False)
    data_encarreiramento = models.DateTimeField(null=False, blank=False)
    cargo_anterior = models.CharField(max_length=100, blank=False, null=False)
    cargo_atual = models.CharField(max_length=100, blank=False, null=False)
    filial_anterior = models.CharField(max_length=100, blank=False, null=False)
    filial_atual = models.CharField(max_length=100, blank=True, null=True)
    data_envio = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_encarreiramentos'
