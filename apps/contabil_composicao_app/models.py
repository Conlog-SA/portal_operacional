from django.db import models

from apps.estrut_org_app.models import Empresa
from apps.usuario_app.models import Usuario


class Pacote_Conta(models.Model):
    cod_pacote_conta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_pacote_conta  = models.CharField(max_length=30, blank=False, null=False)
    obs_pacotes = models.CharField(max_length=100, blank=True, null=True)
    cod_modelo = models.IntegerField(blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'op_contabil_comp_pac_conta'


class Conta(models.Model):
    cod_conta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_conta_contabil_cp = models.IntegerField(blank=False, null=False)
    cod_red_conta_contabil_cp = models.IntegerField(blank=False, null=False)
    handle_conta_financeira_cp = models.IntegerField(blank=True, null=True)
    cod_estrut_cp = models.CharField(max_length=30, null=True, blank=True)
    handle_conta_contabil_lp = models.IntegerField(blank=False, null=False)
    cod_red_conta_contabil_lp = models.IntegerField(blank=False, null=False)
    handle_conta_financeira_lp = models.IntegerField(blank=True, null=True)
    cod_estrut_lp = models.CharField(max_length=30, null=True, blank=True)
    desc_conta = models.CharField(max_length=80, blank=False, null=False)
    tipo_modelo = models.IntegerField(blank=False, null=False)
    data_ini_atividade = models.DateTimeField(blank=True, null=True)
    data_fim_atividade = models.DateTimeField(blank=True, null=True)
    status_comp = models.CharField(max_length=1, blank=True, null=True)
    cod_pacote_conta = models.ForeignKey(Pacote_Conta, models.DO_NOTHING, db_column='cod_pacote_conta', blank=True,
                                         null=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_comp_contas'


class Responsaveis_Conta(models.Model):
    cod_resp_conta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    resp_composicao = models.CharField(max_length=60, blank=True, null=True)
    resp_validacao = models.CharField(max_length=60, blank=True, null=True)
    data_ini_atividade = models.DateTimeField(blank=True, null=True)
    data_fim_atividade = models.DateTimeField(blank=True, null=True)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='cod_empresa', null=True)
    cod_conta = models.ForeignKey(Conta, models.DO_NOTHING, db_column='cod_conta')
    class Meta:
        managed = True
        db_table = 'op_contabil_resp_conta'

class Contrato(models.Model):
    cod_contrato = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_fn_doc = models.IntegerField(blank=False, null=False)
    num_contrato = models.CharField(max_length=45, blank=False, null=False)
    data_emissao_contrato = models.DateTimeField(blank=True, null=True)
    nome_fornecedor = models.CharField(max_length=150, blank=True, null=True)
    handle_operacao = models.IntegerField(blank=True, null=True)
    desc_op = models.CharField(max_length=60, blank=True, null=True)
    num_doc_contabil = models.CharField(max_length=45, blank=True, null=True)
    val_nominal = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    val_liquido = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    sincronizar_benner = models.CharField(max_length=1, blank=True, null=True, default='S')
    dia_util = models.IntegerField(blank=True, null=True)
    data_primeira_parcela = models.DateTimeField(blank=True, null=True)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='cod_empresa', null=True)
    qtd_parcelas = models.IntegerField(blank=True, null=True)
    cod_conta = models.ForeignKey(Conta, models.DO_NOTHING, db_column='cod_conta')
    class Meta:
        managed = True
        db_table = 'op_contabil_comp_contratos'


class Anexos_Contrato(models.Model):
    cod_anexo_contrato = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_competencia = models.DateField(blank=True, null=True)
    desc_anexo = models.CharField(max_length=80, blank=False, null=False)
    caminho_anexo = models.CharField(max_length=200, blank=False, null=False)
    ordem_anexo = models.IntegerField(null=False, blank=False)
    cod_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='cod_contrato', null=True, blank=True)
    cod_conta = models.ForeignKey(Conta, models.DO_NOTHING, db_column='cod_conta', null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_anexos_contrato'

class Parcela_Contrato(models.Model):
    cod_parcela_contrato = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_parcela = models.IntegerField(blank=True, null=True)
    ap_parcela = models.IntegerField(blank=True, null=True)
    ordem_parcela = models.CharField(max_length=10, blank=False, null=False)
    val_conta = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    val_corrigido = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    val_principal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    val_taxas = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    val_fundo = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    natureza = models.CharField(max_length=60, blank=True, null=True)
    data_vencimento = models.DateField(blank=True, null=True)
    tipo_prazo = models.CharField(max_length=2, blank=True, null=True)
    atualiza_benner = models.CharField(max_length=1, blank=False, null=False)
    data_liquidacao = models.DateField(blank=True, null=True)
    val_pago = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cod_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='cod_contrato')
    class Meta:
        managed = True
        db_table = 'op_contabil_comp_parcelas_contratos'



class Auditoria_Status_Composicao_Competencia(models.Model):
    cod_auditoria_composicao = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    status = models.IntegerField(blank=True, null=True)
    tipo_prazo = models.CharField(max_length=2, blank=True, null=True)
    data_lan_auditoria = models.DateField(auto_now_add=True)
    data_competencia = models.DateField(blank=True, null=True)
    val_composicao = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    val_balancete = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    val_diferenca = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    obs_status = models.CharField(max_length=300, blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    cod_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='cod_contrato', null=True, blank=True)
    cod_conta = models.ForeignKey(Conta, models.DO_NOTHING, db_column='cod_conta', null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_auditorias_status_composicao'


class Campos_Contas_Modelo_1(models.Model):
    cod_campo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_campo = models.CharField(max_length=30, blank=True, null=True)
    tipo_campo = models.CharField(max_length=1, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_campos_contas_modelo_1'


class Layout_Importacao_Contas_Modelo_1(models.Model):
    cod_layout = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_layout = models.CharField(max_length=70, blank=True, null=True)
    data_ini_vig = models.DateField(blank=True, null=True)
    data_fim_vig = models.DateField(blank=True, null=True)
    qtd_campos = models.IntegerField(blank=False, null=True)
    tipo_pesq = models.CharField(max_length=1, blank=False, null=False)
    cod_pacote_conta = models.ForeignKey(Pacote_Conta, models.DO_NOTHING, db_column='cod_pacote_conta',
                                         null=True)
    cod_empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='cod_empresa', null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    class Meta:
        managed = True
        db_table = 'op_contabil_layout_imp_contas_modelo_1'


class Layout_Campos_Contas_Modelo_1(models.Model):
    cod_lay_pac_camp = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    num_posicao_campo = models.IntegerField(blank=True, null=True)
    cod_layout = models.ForeignKey(Layout_Importacao_Contas_Modelo_1, models.DO_NOTHING, db_column='cod_layout',
                                   null=True)
    cod_campo = models.ForeignKey(Campos_Contas_Modelo_1, models.DO_NOTHING, db_column='cod_campo',
                                   null=True)

    class Meta:
        managed = True
        db_table = 'op_contabil_lay_camp_contas_modelo_1'


class Arquivo_Docs_Contas_Modelo_1(models.Model):
    cod_arquivo = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    qtd_reg_imp = models.IntegerField(blank=True, null=True)
    data_imp = models.DateTimeField(auto_now_add=True)
    nome_arqv_original = models.CharField(max_length=200, blank=False, null=False)
    nome_arquivo_importado = models.CharField(max_length=200, blank=False, null=False)
    erro = models.CharField(max_length=1, blank=False, null=False)
    data_competencia = models.DateField(blank=True, null=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    cod_conta = models.ForeignKey(Conta, models.DO_NOTHING, db_column='cod_conta', null=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_arqv_imp_contas_m1'


class Registros_Arqv_Docs_Contas_Modelo_1(models.Model):
    cod_reg = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    num_linha = models.IntegerField(blank=False, null=False)
    val_linha = models.CharField(max_length=200, blank=False, null=False)
    cod_lay_pac_camp = models.ForeignKey(Layout_Campos_Contas_Modelo_1, models.DO_NOTHING, db_column='cod_lay_pac_camp',
                                         null=True)
    cod_arquivo = models.ForeignKey(Arquivo_Docs_Contas_Modelo_1, models.DO_NOTHING, db_column='cod_arquivo',
                                    null=True)
    class Meta:
        managed = True
        db_table = 'op_contabil_reg_arqv_contas_m1'







