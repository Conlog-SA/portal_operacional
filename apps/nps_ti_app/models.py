from django.db import models

class Filial_Nps(models.Model):
    cod_filial_nps = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_filial_nps = models.CharField(max_length=50, blank=True, null=True)
    cod_empresa_nps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_nps_ti_filial'

class Pesquisa_Satisfacao(models.Model):
    cod_pesquisa = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_filial_nps = models.ForeignKey(Filial_Nps, models.DO_NOTHING, db_column='cod_filial_nps', blank=True,
                                         null=True)
    questoes_respondidas = models.CharField(max_length=2500, blank=True, null=True)
    email = models.CharField(max_length=100, blank=False, null=False)
    data_resposta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_nps_ti_pesquisa'

class Email_Enviado_Nps(models.Model):
    cod_envio_email = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    data_envio = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_nps_ti_email'