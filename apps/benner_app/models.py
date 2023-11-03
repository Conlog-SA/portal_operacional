from django.db import models

class Placa_Beneficiario_Terceiro():
    def __init__(self, handle_benef, nome_benef, tipo_benef, status_benef, doc_benef, handle_placa, placa, status_placa,
                 perfil_placa, status_cadastro_bd_operacional):
        self.handle_benef = handle_benef
        self.nome_benef = nome_benef
        self.tipo_benef = tipo_benef
        self.status_benef = status_benef
        self.doc_benef = doc_benef
        self.handle_placa = handle_placa
        self.placa = placa
        self.status_placa = status_placa
        self.perfil_placa = perfil_placa
        self.status_cadastro_bd_operacional = status_cadastro_bd_operacional

from django.db import models

class Empresa_Benner():
    def __init__(self,handle_emp, cod_emp, estrut_emp, nome_emp):
        self.handle_emp = handle_emp
        self.cod_emp = cod_emp
        self.estrut_emp = estrut_emp
        self.nome_emp = nome_emp

class Operacao_Benner():
    def __init__(self, handle_op, cod_emp, estrut_emp, estrut_op, nome_op):
        self.handle_op = handle_op
        self.cod_emp = cod_emp
        self.estrut_emp = estrut_emp
        self.estrut_op = estrut_op
        self.nome_op = nome_op


class Filial_Benner():
    def __init__(self, handle_filial, cod_emp, estrut_emp, estrut_op, estrut_filial, nome_filial):
        self.handle_filial = handle_filial
        self.cod_emp = cod_emp
        self.estrut_emp = estrut_emp
        self.estrut_op = estrut_op
        self.estrut_filial = estrut_filial
        self.nome_filial = nome_filial

class Projeto_Benner():
    def __init__(self, handle_proj, cod_emp, estrut_emp, estrut_op, estrut_filial, estrut_proj, nome_proj):
        self.handle_proj = handle_proj
        self.cod_emp = cod_emp
        self.estrut_emp = estrut_emp
        self.estrut_op = estrut_op
        self.estrut_filial = estrut_filial
        self.estrut_proj = estrut_proj
        self.nome_proj = nome_proj

class DRE_SINTETICO():
    def __init__(self, COMPETENCIA, Dre_Conta_Rel_Estrut_Dre, VALOR):
        self.COMPETENCIA                =   COMPETENCIA
        self.Dre_Conta_Rel_Estrut_Dre   =   Dre_Conta_Rel_Estrut_Dre
        self.VALOR                      =   VALOR


class Historico_Razao_Conta():
    def __init__(self, competencia, data_lanc, handle_projeto, nome_projeto, handle_conta, k_contacontabilmaxys, val_lanc, sub_conta, nome_fornecedor, num_doc, placa, historico, natureza):
        self.competencia                =   competencia
        self.data_lanc                  =   data_lanc
        self.handle_projeto             =   handle_projeto
        self.nome_projeto               =   nome_projeto
        self.handle_conta               =   handle_conta
        self.k_contacontabilmaxys              =   k_contacontabilmaxys
        self.val_lanc                   =   val_lanc
        self.sub_conta                  =   sub_conta
        self.nome_fornecedor            =   nome_fornecedor
        self.num_doc                    =   num_doc
        self.placa                      =   placa
        self.historico                  =   historico
        self.natureza                   =   natureza


class RegistroNotaBenner():
    def __init__(self, numDoc,serieDoc,dataEmissaoDoc,placa,valorDoc,	statusDoc,cnpjRemetente,descRemetente,
                 cnpjDestinatario,descDestinatario,cidadeOrigem,cidadeDestino,codDT,codVBZ,nomeTransp,razaoOrigem,
                 razaoDestino,chaveDoc,chaveCTE,cnpjTomadorServico,docRef,tipoCTE,observacao,kNegocioMaxys):
        self.numDoc = numDoc
        self.serieDoc = serieDoc
        self.dataEmissaoDoc = dataEmissaoDoc
        self.placa = placa
        self.valorDoc = valorDoc
        self.statusDoc = statusDoc
        self.cnpjRemetente = cnpjRemetente
        self.descRemetente = descRemetente
        self.cnpjDestinatario = cnpjDestinatario
        self.descDestinatario = descDestinatario
        self.cidadeOrigem = cidadeOrigem
        self.cidadeDestino = cidadeDestino
        self.codDT = codDT
        self.codVBZ = codVBZ
        self.nomeTransp = nomeTransp
        self.razaoOrigem = razaoOrigem
        self.razaoDestino = razaoDestino
        self.chaveDoc = chaveDoc
        self.chaveCTE = chaveCTE
        self.cnpjTomadorServico = cnpjTomadorServico
        self.docRef = docRef
        self.tipoCTE = tipoCTE
        self.observacao = observacao
        self.kNegocioMaxys = kNegocioMaxys


class Requisicao_Atendidas_TMA():
    def __init__(self, handle_filial, nome_filial, cod_empresa, cnpj_filial, handle_req_pai, num_req_pai, data_inclusao, data_confirmada,
                 data_atendida, handle_usu_incluiu, nome_usu_incluiu, handle_familia, desc_familia, status_ordem,
                 cod_comprador, nome_comprador, data_atendida_prevista, tma, tma_previsto,
                 status_atendimento, status_importacao):
        self.handle_filial = handle_filial
        self.nome_filial = nome_filial
        self.cod_empresa = cod_empresa
        self.cnpj_filial = cnpj_filial
        self.handle_req_pai = handle_req_pai
        self.num_req_pai = num_req_pai
        self.data_inclusao = data_inclusao
        self.data_confirmada = data_confirmada
        self.data_atendida = data_atendida
        self.handle_usu_incluiu = handle_usu_incluiu
        self.nome_usu_incluiu = nome_usu_incluiu
        self.handle_familia = handle_familia
        self.desc_familia = desc_familia
        self.status_ordem = status_ordem
        self.cod_comprador = cod_comprador
        self.nome_comprador = nome_comprador
        self.data_atendida_prevista = data_atendida_prevista
        self.tma = tma
        self.tma_previsto = tma_previsto
        self.status_atendimento = status_atendimento
        self.status_importacao = status_importacao


class Empilhadeira():
    def __init__(self, handle, placa, desc, ano, modelo, placa_anterior, ativo):
        self.handle = handle
        self.placa = placa
        self.desc = desc
        self.ano = ano
        self.modelo = modelo
        self.placa_anterior = placa_anterior
        self.ativo = ativo


class Equipamentos():
    def __init__(self, handle, placa, desc, ano, modelo, placa_anterior, ativo):
        self.handle = handle
        self.placa = placa
        self.desc = desc
        self.ano = ano
        self.modelo = modelo
        self.placa_anterior = placa_anterior
        self.ativo = ativo


class Ordens_Servico():
    def __init__(self, handle, numero, handle_tipo, desc_tipo, data_ini, data_fim, handle_conjunto, desc_conjunto,
                 desc_os, situacao, vinculada):
        self.handle = handle
        self.numero = numero
        self.handle_tipo = handle_tipo
        self.desc_tipo = desc_tipo
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.handle_conjunto  = handle_conjunto
        self.desc_conjunto = desc_conjunto
        self.desc_os = desc_os
        self.situacao = situacao
        self.vinculada = vinculada


class Comprador():
    def __init__(self, handle, nome):
        self.handle = handle
        self.nome = nome

class Beneficiario_Terceiro():
    def __init__(self, handle, nome, tipo, inativo, doc, qtd_placas):
        self.handle = handle
        self.nome = nome
        self.tipo = tipo
        self.inativo = inativo
        self.doc = doc
        self.qtd_placas = qtd_placas


class Evolucao_Preco_Itens_Tres_Ultimas_Compras():
    def __init__(self, cod_ref_item, desc_item, desc_variacao, desc_familia, val_antepenultima,
                 dados_antepenultima_compra, val_penultima, dados_penultima_compra, val_ultima,
                 dados_ultima_compra, perc_dispersao, analise, val_dispersao, handle_filial, nome_filial, val_evolucao):
        self.cod_ref_item = cod_ref_item
        self.desc_item = desc_item
        self.desc_variacao = desc_variacao
        self.desc_familia = desc_familia
        self.val_antepenultima = val_antepenultima
        self.dados_antepenultima_compra = dados_antepenultima_compra
        self.val_penultima = val_penultima
        self.dados_penultima_compra = dados_penultima_compra
        self.val_ultima = val_ultima
        self.dados_ultima_compra = dados_ultima_compra
        self.perc_dispersao = perc_dispersao
        self.analise = analise
        self.val_dispersao = val_dispersao
        self.handle_filial = handle_filial
        self.nome_filial = nome_filial
        self.val_evolucao = val_evolucao


class Compras_Item():
    def __init__(self, handle_filial_compra,nome_filial_compra,cod_ref_prod,handle_produto,nome_produto,desc_variacao,
                 handle_familia,desc_familia,val_unit,handle_variacao,handle_compra,numero_compra,data_compra,
                 handle_usuario_incluiu_compra,nome_usuario_incluiu_compra,handle_fornecedor_comra,
                 nome_fornecedor_compra,doc_fornecedor_compra,qtd_item,val_tt_item,nome_un_medida,numero_req,data_req,
                 status_req,desc_tipo_compra_req,handle_itens_compra,handle_req,handle_req_pai,
                 handle_cidade_fornecedor,nome_cidade_fornecedor, uf_fornecedor):
        self.handle_filial_compra = handle_filial_compra
        self.nome_filial_compra = nome_filial_compra
        self.cod_ref_prod = cod_ref_prod
        self.handle_produto = handle_produto
        self.nome_produto = nome_produto
        self.desc_variacao = desc_variacao
        self.handle_familia = handle_familia
        self.desc_familia = desc_familia
        self.val_unit = val_unit
        self.handle_variacao = handle_variacao
        self.handle_compra = handle_compra
        self.numero_compra = numero_compra
        self.data_compra = data_compra
        self.handle_usuario_incluiu_compra = handle_usuario_incluiu_compra
        self.nome_usuario_incluiu_compra = nome_usuario_incluiu_compra
        self.handle_fornecedor_comra = handle_fornecedor_comra
        self.nome_fornecedor_compra = nome_fornecedor_compra
        self.doc_fornecedor_compra = doc_fornecedor_compra
        self.qtd_item = qtd_item
        self.val_tt_item = val_tt_item
        self.nome_un_medida = nome_un_medida
        self.numero_req = numero_req
        self.data_req = data_req
        self.status_req = status_req
        self.desc_tipo_compra_req = desc_tipo_compra_req
        self.handle_itens_compra = handle_itens_compra
        self.handle_req = handle_req
        self.handle_req_pai = handle_req_pai
        self.handle_cidade_fornecedor = handle_cidade_fornecedor
        self.nome_cidade_fornecedor = nome_cidade_fornecedor
        self.uf_fornecedor = uf_fornecedor

class Familia():
    def __init__(self, handle, nome):
        self.handle = handle
        self.nome = nome

class Produto():
    def __init__(self, handle, nome, cod_ref):
        self.handle = handle
        self.nome = nome
        self.cod_ref = cod_ref