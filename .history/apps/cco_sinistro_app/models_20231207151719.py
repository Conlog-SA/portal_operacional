from django.db import models
from apps.usuario_app.models import Usuario, Projeto, Filial
from apps.estrut_org_app.models import OP_Estados

class Motivo_Sinistro(models.Model):
    cod_motivo_sinistro = models.AutoField(primary_key=True, editable=False, auto_created=True)
    desc_motivo_sinistro = models.CharField(max_length=50, null=False, blank=False)
    tipo_motivo_sinistro = models.CharField(max_length=1, null=False, blank=False)
    class Meta():
        managed = True
        db_table = 'ger_cco_motivos_sinistros'

class CCO_Sinistro(models.Model):
    cod_sinistro = models.AutoField(primary_key=True, editable=False, auto_created=True)
    nome_mot = models.CharField(max_length=80, null=False, blank=False)
    status_processo = models.CharField(max_length=10, null=False, blank=False)
    data_inclusao = models.DateField(max_length=15, null=False, blank=False)
    cpf_mot = models.CharField(max_length=11, null=True, blank=True)
    placa_veiculo_cavalo = models.CharField(max_length=12, null=False, blank=False)
    data_nasc = models.DateField(null=True, blank=True)
    data_ocorre_sinistro = models.DateField(null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    acionado_seguro = models.CharField(max_length=3, null=True, blank=True, default='S')
    data_inicio_processo = models.DateField(null=True, blank=True)
    data_fim_processo = models.DateField(null=True, blank=True)
    num_processo = models.CharField(max_length=15, null=True, blank=True)
    tipo_sinistro = models.CharField(null=True, blank=True, max_length=20)
    obs = models.CharField(max_length=300, null=True, blank=True)
    cod_motivo_sinistro = models.ForeignKey(Motivo_Sinistro, models.DO_NOTHING, db_column='cod_motivo_sinistro')
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=True, blank=True)
    cod_estado = models.ForeignKey(OP_Estados, models.DO_NOTHING, db_column='cod_estado', null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed = True
        db_table = 'ger_cco_sinistros'




class CCO_Sinistro_Carga(models.Model):
    cod_sinistro_carga = models.AutoField(primary_key=True, editable=False, auto_created=True)
    empresa = models.CharField(null=False, blank=False, max_length=20)
    tipo_frota = models.CharField(null=False, blank=False, max_length=10)
    transportador = models.CharField(null=False, blank=False, max_length=10)
    placa_veiculo_carreta = models.CharField(null=True, blank=True, max_length=10)
    tipo_veiculo = models.CharField(null=False, blank=False, max_length=12)
    cliente = models.CharField(null=False, blank=False, max_length=10)
    tipo_mercadoria = models.CharField(null=False, blank=False, max_length=12)
    num_nota_fiscal = models.CharField(null=True, blank=True, max_length=6)
    cte_serie = models.CharField(null=True, blank=True, max_length=10)
    valor_tot_produtos = models.CharField(null=True, blank=True, max_length=12)
    hora_sinistro = models.TimeField(null=True, blank=True)
    local_ocorre_sinistro = models.CharField(null=True, blank=True, max_length=30)
    valor_sinistro = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    resp_seguro = models.CharField(null=True, blank=True, max_length=200)
    seguradora = models.CharField(null=True, blank=True, max_length=20)
    reguladora = models.CharField(null=True, blank=True, max_length=30)
    reembolso = models.CharField(max_length=1, null=True, blank=True, default='S')
    val_reembolso = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    data_abertura_registro_sinistro = models.DateField(null=True, blank=True)
    data_fechamento_registro_sinistro = models.DateField(null=True, blank=True)
    status_doc = models.CharField(null=False, blank=True, max_length=20)
    cod_sinistro = models.ForeignKey(CCO_Sinistro, models.CASCADE, db_column='cod_sinistro')
    class Meta():
        managed = True
        db_table = 'ger_cco_sinistros_cargas'



class CCO_Sinistro_Equipamento(models.Model):
    cod_sinistro_equipamento = models.AutoField(primary_key=True, editable=False, auto_created=True)
    data_comunicacao_seguradora = models.DateField(null=True, blank=True)
    data_comunicacao_cco = models.DateField(null=True, blank=True)
    resp_dano = models.CharField(max_length=30, null=True, blank=True)
    descontado_colab = models.CharField(max_length=5, null=True, blank=False, default='S')
    indenizado = models.CharField(max_length=3, null=True, blank=True, default='S')
    houve_danos_emp = models.CharField(max_length=1, null=True, blank=True, default='S')
    val_indenizado = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    val_prejuizo = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    resp_indenizar_dano = models.CharField(max_length=30, null=True, blank=True)
    cod_sinistro = models.ForeignKey(CCO_Sinistro, models.CASCADE, db_column='cod_sinistro')
    tipo_acionamento = models.CharField(max_length=30, null=True, blank=True)
    feito_reembolso_eqp = models.CharField(max_length=3, null=True, blank=True)
    class Meta():
        managed = True
        db_table = 'ger_cco_sinistros_equipamentos'



