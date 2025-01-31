import io

from django.db import models
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from apps.estrut_org_app.models import Projeto
from apps.frota_importa_2art_app.models import Registro2Art
from apps.usuario_app.models import Usuario


class BeneficiarioTerceiro(models.Model):
    cod_benef_terc = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    nome_benef_terc = models.CharField(max_length=150, null=True)
    doc_benef_terc = models.CharField(max_length=20, null=True)
    tipo_pessoa_benef_terc = models.CharField(max_length=20, null=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    status_benef = models.CharField(max_length=1,default='A')
    data_status = models.DateField(auto_now_add=True, null=True)
    handle_benner = models.IntegerField(blank=False, null=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True)
    class Meta:
        managed = True
        db_table = 'ger_cad_beneficiario_terc'#op_plan_controle_cad_beneficiario_terc'


class CadFreteSpot(models.Model):
    cod_cad_frete_spot = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    tipo_entrega = models.CharField(max_length=4, null=True, blank=True)
    data_ini_vigencia = models.DateField(null=True)
    data_fim_vigencia = models.DateField(null=True)
    tipo_perfil_veiculo = models.CharField(max_length=15, null=True, blank=True)
    cod_regiao = models.IntegerField()
    nome_regiao = models.CharField(max_length=80, null=True, blank=True)
    qtd_min = models.IntegerField()
    val_frete_carreteiro_min = models.DecimalField(max_digits=8, decimal_places=2)
    val_descarga_min = models.DecimalField(max_digits=8, decimal_places=2)
    val_pedagio_min = models.DecimalField(max_digits=8, decimal_places=2)
    val_cprb_min = models.DecimalField(max_digits=8, decimal_places=2)
    val_lucro_min = models.DecimalField(max_digits=8, decimal_places=2)
    qtd_max = models.IntegerField()
    val_frete_carreteiro_max = models.DecimalField(max_digits=8, decimal_places=2)
    val_descarga_max = models.DecimalField(max_digits=8, decimal_places=2)
    val_pedagio_max = models.DecimalField(max_digits=8, decimal_places=2)
    val_cprb_max = models.DecimalField(max_digits=8, decimal_places=2)
    val_lucro_max = models.DecimalField(max_digits=8, decimal_places=2)
    tipo_pessoa = models.CharField(max_length=20, null=True, blank=True)
    class Meta():
        managed = True
        db_table = 'ger_cad_frete_spot'#op_plan_controle_cad_frete_spot'
        unique_together = ('tipo_entrega', 'data_ini_vigencia','data_fim_vigencia', 'tipo_perfil_veiculo', 'cod_regiao', 'qtd_min', 'qtd_max', 'tipo_pessoa', 'cod_projeto')



class CadastroPlacaTerceiro(models.Model):
    cod_cad_placa_terc = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    placa_cad_placa_terc = models.CharField(max_length=50, null=True)
    perfil_veiculo_cad_placa_terc = models.CharField(max_length=50, null=True)
    handle_benner = models.IntegerField(blank=False, null=False)
    data_ini_vigencia = models.DateField(null=True)
    data_fim_vigencia = models.DateField(null=True)
    cod_benef_terc = models.ForeignKey(BeneficiarioTerceiro, models.DO_NOTHING, db_column='cod_benef_terc')
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    class Meta:
        managed = True
        db_table = 'ger_cad_placa_terceiro'#op_plan_controle_cad_placa_terceiro'
        unique_together = ('placa_cad_placa_terc', 'perfil_veiculo_cad_placa_terc', 'data_ini_vigencia', 'data_fim_vigencia', 'cod_projeto', 'cod_benef_terc')


class TipoOcorrenciasFinanceiroTerceiros(models.Model):
    cod_tipo_ocor_financ_terc = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_ocorrencia = models.CharField(max_length=80)
    tipo_lancamento = models.CharField(max_length=1)
    class Meta():
        managed = True
        db_table = 'ger_tipo_ocor_financ_terc'#op_plan_controle_tipo_ocor_financ_terc'


class Pagamento2ArtTerceirosFinanceiro(models.Model):
    cod_pag_2art_terc_financ = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    valor_frete_calc_pag = models.DecimalField(max_digits=8, decimal_places=2)
    desc_pag = models.DecimalField(max_digits=8, decimal_places=2)
    acresc_pag = models.DecimalField(max_digits=8, decimal_places=2)
    val_pago = models.DecimalField(max_digits=8, decimal_places=2)
    val_conlog = models.DecimalField(max_digits=8, decimal_places=2)
    periodo_ref_pag = models.DateField(null=True)
    data_geracao_pag = models.DateField(null=True)
    obs_pag = models.CharField(max_length=500, null=True)
    complemento_pag = models.CharField(max_length=100, null=True)
    status_pagamento = models.CharField(max_length=1, null=True, default='G')
    num_doc_pagamento = models.IntegerField(null=True)
    cod_tipo_ocor_financ_terc = models.ForeignKey(TipoOcorrenciasFinanceiroTerceiros, models.DO_NOTHING, db_column='cod_tipo_ocor_financ_terc',null=True, blank=True)
    cod_benef_terc = models.ForeignKey(BeneficiarioTerceiro, models.DO_NOTHING, db_column='cod_benef_terc')
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    class Meta():
        managed = True
        db_table = 'ger_pagamento_2art_terc_financ'#op_plan_controle_pag_2art_terc_financ'




class Registro2ArtTerceirosFinanceiro(models.Model):
    cod_reg_2art_terc_financ = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_2art_terc_financ = models.DateField(null=True)
    transp_2art_terc_financ = models.CharField(max_length=50,null=True)
    entrega_2art_terc_financ = models.CharField(max_length=50,null=True)
    cargaatual_2art_terc_financ = models.CharField(max_length=50,null=True)
    codfilial_2art_terc_financ = models.CharField(max_length=50,null=True)
    frota_2art_terc_financ = models.CharField(max_length=50,null=True)
    custospot_2art_terc_financ = models.CharField(max_length=50,null=True)
    regiaospot_2art_terc_financ = models.CharField(max_length=50,null=True)
    placa_2art_terc_financ = models.CharField(max_length=50,null=True)
    mapa_2art_terc_financ = models.CharField(max_length=50,null=True)
    entregas_2art_terc_financ = models.CharField(max_length=50,null=True)
    valorfrete_2art_terc_financ = models.CharField(max_length=50,null=True)
    tipoimposto_2art_terc_financ = models.CharField(max_length=50,null=True)
    percimposto_2art_terc_financ = models.CharField(max_length=50,null=True)
    valorimposto_2art_tercfinanc = models.CharField(max_length=50,null=True)
    valorfaturado_2art_terc_financ = models.CharField(max_length=50,null=True)
    nomespot_2art_terc_financ = models.CharField(max_length=50,null=True)
    data_importacao_2art_terc_financ = models.DateField(auto_now_add=True)
    qtd_subscrita_2art_terc_financ = models.IntegerField(default=0)
    data_ultima_subscricao_2art_terc_financ = models.DateField(null=True)
    status_financeiro_2art_terc_financ = models.CharField(max_length=1,null=True)
    data_status_financeiro_2art_terc_financ = models.DateField(null=True)
    status_mapa_2art_terc_financ = models.CharField(max_length=1,null=True)
    valor_frete_calculado_pago = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    val_a_pagar_pago = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    val_conlog_pago = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    cod_reg_2art = models.ForeignKey(Registro2Art, models.DO_NOTHING, db_column='cod_reg_2art')
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    cod_cad_placa_terc = models.ForeignKey(CadastroPlacaTerceiro, models.DO_NOTHING, db_column='cod_cad_placa_terc',null=True, blank=True)
    cod_pag_2art_terc_financ = models.ForeignKey(Pagamento2ArtTerceirosFinanceiro, models.DO_NOTHING, db_column='cod_pag_2art_terc_financ',null=True, blank=True)
    cod_cad_frete_spot = models.ForeignKey(CadFreteSpot, models.DO_NOTHING, db_column='cod_cad_frete_spot', null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'ger_2art_terceiros_financeiro'#op_plan_controle_2art_terc_financeiro'



class  HistAcaoMapas2ArtTerceiros(models.Model):
    cod_reg_hist_acao_mapa_terc = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_hist_acao_mapa_terc = models.DateField(auto_now_add=True)
    acao_hist_acao_mapa_terc = models.CharField(max_length=1, blank=False, null=False)
    obs_hist_acao_mapa_terc = models.CharField(max_length=250, blank=False, null=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=False, blank=False)
    cod_reg_2art_terc_financ = models.ForeignKey(Registro2ArtTerceirosFinanceiro, models.DO_NOTHING,
                                                 db_column='cod_reg_2art_terc_financ', null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'ger_2art_hist_acoes_mapas_terc'#op_plan_controle_2art_hist_acoes_mapas_terc'


class LancamentosRegistro2ArtTerceirosFinanceiro(models.Model):
    cod_lanc_2art_terc_financ = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    mapa_ocorrencia = models.CharField(max_length=6, null=True, blank=True)
    placa_lanc = models.CharField(max_length=10,null=True)
    data_ocorrencia = models.DateField(null=True)
    valor_lanc = models.DecimalField(max_digits=8, decimal_places=2)
    tipo_lancamento = models.CharField(max_length=1, null=False, blank=False)
    data_lanc = models.DateField(null=True)
    obs_lanc = models.CharField(max_length=100, null=True, blank=True)
    status_exclusao = models.CharField(max_length=1, null=True)
    cod_reg_2art_terc_financ = models.ForeignKey(Registro2ArtTerceirosFinanceiro, models.DO_NOTHING, db_column='cod_reg_2art_terc_financ',null=True, blank=True)
    cod_tipo_ocor_financ_terc = models.ForeignKey(TipoOcorrenciasFinanceiroTerceiros, models.DO_NOTHING, db_column='cod_tipo_ocor_financ_terc',null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    class Meta():
        managed = True
        db_table = 'ger_lancamentos_registro_2art_terc_financ'#op_plan_controle_lancamentos_registro_2art_terc_financ'


class LancamentoPagamentoExtras(models.Model):
    cod_lanc_pag_extra = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_pag_extra = models.DateField(null=True)
    mapa_pag_extra = models.CharField(max_length=8, null=True, blank=True)
    placa_pag_extra = models.CharField(max_length=7, null=True, blank=True)
    desc_pag_extra = models.DecimalField(max_digits=8, decimal_places=2)
    acresc_pag_extra = models.DecimalField(max_digits=8, decimal_places=2)
    val_pag_extra = models.DecimalField(max_digits=8, decimal_places=2)
    periodo_ref_pag_extra = models.DateField(null=True)
    obs_pag_extra = models.CharField(max_length=300, null=True)
    data_imp = models.DateField(auto_now_add=True)
    cod_tipo_ocor_financ_terc = models.ForeignKey(TipoOcorrenciasFinanceiroTerceiros, models.DO_NOTHING,
                                                  db_column='cod_tipo_ocor_financ_terc', null=True, blank=True)
    cod_pag_2art_terc_financ = models.ForeignKey(Pagamento2ArtTerceirosFinanceiro, models.DO_NOTHING,
                                                 db_column='cod_pag_2art_terc_financ', null=True, blank=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed=True
        db_table='ger_lancamentos_pagamento_extras'#op_plan_controle_lancamentos_pagamento_extras'


class Estorno_Pagamentos_2Art_Terc(models.Model):
    cod_estorno_pag_2art_terc = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    tipo_pagamento = models.CharField(max_length=1, null=False, blank=False, default='')#E: Extra, pagamento extra / M: pagamento mapas
    cod_pagamento_referente = models.IntegerField(null=False, blank=False)
    data_hora_estorno = models.DateTimeField()
    justificativa = models.CharField(max_length=300, null=False, blank=False)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu', null=True, blank=True)
    class Meta():
        managed=True
        db_table='op_plan_controle_pag_terc_estorno_pagamentos'

class Tab_Cad_Placa_Terc_Financ():
    def __init__(self, id_cad_placa_terc, placa, perfil_veic, handle_placa, nome_beneficiario, doc_benef, tipo_pessoa_benef,
                 handle_benef, data_ini, data_fim, ):
        self.id_cad_placa_terc = id_cad_placa_terc
        self.placa = placa
        self.perfil_veic = perfil_veic
        self.handle_placa = handle_placa
        self.nome_beneficiario = nome_beneficiario
        self.doc_benef = doc_benef
        self.tipo_pessoa_benef = tipo_pessoa_benef
        self.handle_benef = handle_benef
        self.data_ini = data_ini
        self.data_fim = data_fim



class LinhaExcelArquivoLanAcresDesc():
    def __init__(self, cod_lanc_banco, serial_proj, desc_tipo_lanc, desc_ocorrencia_lan, mapa_ocorrencia,
                 data_ocorrencia, mapa, placa, valor, observacao, status_importacao):
        self.cod_lanc_banco = cod_lanc_banco
        self.serial_proj = serial_proj
        self.desc_tipo_lanc = desc_tipo_lanc
        self.desc_ocorrencia_lan = desc_ocorrencia_lan
        self.mapa_ocorrencia = mapa_ocorrencia
        self.data_ocorrencia = data_ocorrencia
        self.mapa = mapa
        self.placa = placa
        self.valor = valor
        self.observacao = observacao
        self.status_importacao = status_importacao


class LinhaExcelArquivoPagamentosExtra():
    def __init__(self, cod_lanc_banco, doc_benef, data, mapa, tipo_ocorrencia, placa, desc, acres, valor, periodo_ref,
                 observacao, status_importacao):
        self.cod_lanc_banco = cod_lanc_banco
        self.doc_benef = doc_benef
        self.data = data
        self.mapa = mapa
        self.tipo_ocorrencia = tipo_ocorrencia
        self.placa = placa
        self.desc = desc
        self.acres = acres
        self.valor = valor
        self.periodo_ref = periodo_ref
        self.observacao = observacao
        self.status_importacao = status_importacao




class Tab_Pagamentos_Terceiros():
    def __init__(self, cod_pag, cod_benef, doc_benef, nome_beneficiario, data, mapa, placa,  val_frete, desc, acres,
                 val_pagar, complemento, tipo_ocorrencia, serial_pag_proj, obs_desc, obs_acresc, seq_item, status_pag,
                 nome_usu_status, num_doc_pagamento, nome_usu_estorno, data_estorno, justificativa_estorno):
        self.cod_pag = cod_pag
        self.cod_benef = cod_benef
        self.doc_benef = doc_benef
        self.nome_beneficiario = nome_beneficiario
        self.data = data
        self.mapa = mapa
        self.placa = placa
        self.desc = desc
        self.acres = acres
        self.val_frete = val_frete
        self.val_pagar = val_pagar
        self.complemento = complemento
        self.tipo_ocorrencia = tipo_ocorrencia
        self.serial_pag_proj = serial_pag_proj
        self.obs_desc = obs_desc
        self.obs_acresc = obs_acresc
        self.seq_item = seq_item
        self.status_pag = status_pag
        self.nome_usu_status=nome_usu_status
        self.num_doc_pagamento = num_doc_pagamento
        self.nome_usu_estorno = nome_usu_estorno
        self.data_estorno = data_estorno
        self.justificativa_estorno = justificativa_estorno


class Tab_Lancamentos_Pagamento_Terceiros():
    def __init__(self, tipo_lancamento, desc_ocorrencia, mapa_ocorrencia, data_ocorrencia, mapa, placa,  valor_lanc,
                 obs, seq_item):
        self.tipo_lancamento = tipo_lancamento
        self.desc_ocorrencia = desc_ocorrencia
        self.mapa_ocorrencia = mapa_ocorrencia
        self.data_ocorrencia = data_ocorrencia
        self.mapa = mapa
        self.placa = placa
        self.valor_lanc = valor_lanc
        self.obs = obs
        self.seq_item = seq_item

class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf'
            )
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Erro Rendering PDF", status=400)
