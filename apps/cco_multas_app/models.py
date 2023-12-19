from django.db import models
from apps.usuario_app.models import Usuario, Projeto

class CCO_Tipo_Multa(models.Model):
    cod_tipo_multa = models.AutoField(primary_key=True, editable=False, auto_created=False)
    desc_multa = models.CharField(null=False, editable=False, max_length=50)
    class Meta():
        managed = True
        db_table = 'ger_cco_tipo_multas'

class CCO_Multas(models.Model):
    cod_multa_antt = models.AutoField(primary_key=True, editable=False, auto_created=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    placa_multa = models.CharField(blank=False, max_length=12)
    num_auto_infracao = models.CharField(null=True, blank=True, max_length=20)
    data_auto = models.DateField(null=True, blank=True)
    cod_infracao = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=2)
    data_recebe_multa = models.DateField(null=True, blank=True)
    data_inclusao = models.DateField(null=False, blank=False, auto_created=True, auto_now=True)
    local_multa = models.CharField(null=True, blank=True, max_length=30)
    cod_tipo_multa = models.ForeignKey(CCO_Tipo_Multa, models.CASCADE, db_column='cod_tipo_multa')
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    data_pag_multa = models.DateField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=12)
    valor_pagar = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    nome_condutor = models.CharField(null=True, blank=True, max_length=30)
    obs = models.CharField(null=True, blank=True, max_length=100)
    class Meta():
        managed = True
        db_table = 'ger_cco_multas'

class CCO_Anexos(models.Model):
    cod_anexo_cco = models.AutoField(primary_key=True, editable=False, auto_created=True)
    caminho_anexo = models.CharField(null=False, blank=True, max_length=100)
    cod_multa_antt = models.ForeignKey(CCO_Multas, models.CASCADE, db_column='cod_multa_antt')
    tipo_anexo = models.CharField(null=False, blank=True, max_length=20)
    class Meta():
        managed = True
        db_table = 'ger_cco_anexos'
