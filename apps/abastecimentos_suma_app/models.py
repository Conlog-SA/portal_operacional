from django.db import models

class Abastecimento(models.Model):
    cod_abastecimento = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_hora = models.DateTimeField(blank=True, null=True)
    num_placa = models.CharField(max_length=8, blank=True, null=True)
    num_odometro = models.IntegerField(null=False, blank=-False)
    nom_motorista = models.CharField(max_length=100, blank=True, null=True)
    cpf_motorista = models.CharField(max_length=11, blank=True, null=True)
    des_item = models.CharField(max_length=50, blank=True, null=True)
    nom_centro_manutencao = models.CharField(max_length=150, blank=False, null=False)
    nom_bomba = models.CharField(max_length=150, blank=False, null=False)
    cpf_operador = models.CharField(max_length=11, blank=False, null=False)
    qtd_item = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    comp_tanque = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'op_abastecimentos_suma'
