from django.db import models

class Vincula_Roteiro_Pecas(models.Model):
    #chave composta do handle do roteiro, handle da marca e handle do modelo do Benner
    cod_roteiro_peca = models.IntegerField(primary_key=True, editable=False, blank=False)
    handle_roteiro = models.IntegerField()
    nome_roteiro = models.CharField(max_length=300)
    handle_marca = models.IntegerField()
    nome_marca = models.CharField(max_length=50)
    handle_modelo = models.IntegerField()
    nome_modelo = models.CharField(max_length=100)
    handle_tipo_veiculo = models.IntegerField()
    nome_tipo_veiculo = models.CharField(max_length=100)
    cod_ref_item = models.CharField(max_length=30)
    desc_item = models.CharField(max_length=200)
    un_item = models.CharField(max_length=10)
    qtd = models.IntegerField()
    troca = models.BooleanField()
    data_lancamento = models.DateField(auto_now_add=True)
    class Meta():
        managed = True
        db_table = 'op_frota_vpo_vinculo_roteiro_peca'

