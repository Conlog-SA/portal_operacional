from django.db import models

class Contrato_Processado(models.Model):
    cod_contrato_frete = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    nro_contrato = models.CharField(max_length=100, blank=False, null=False)
    razao_social_contratado = models.CharField(max_length=300, blank=False, null=False)
    data_contrato = models.CharField(max_length=60, blank=False, null=False)
    status = models.CharField(max_length=60, blank=False, null=False)
    nome_arquivo = models.CharField(max_length=300, blank=False, null=False)
    data_processamento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_contratos_frete_deep'