from django.db import models

class Phishing(models.Model):
    cod_envio = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    usuario = models.CharField(max_length=30, blank=True, null=True)
    senha = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=False, null=False)
    data_envio = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_phishing_respondidos'

class Phishing_Enviados(models.Model):
    cod_envio_email = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    data_envio = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_phishing_enviados'