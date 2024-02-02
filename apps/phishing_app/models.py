from django.db import models

class Phishing(models.Model):
    cod_envio = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    usuario = models.CharField(max_length=70, blank=True, null=True)
    senha = models.CharField(max_length=70, blank=True, null=True)
    data_envio = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_phishing'