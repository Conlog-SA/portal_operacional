

class Componente_Colaboradores():
    def __init__(self, id, text, cpf, data_adm, cod_cargo, desc_cargo, sit_colab):
        self.id = id
        self.text = text
        self.cpf = cpf
        self.data_adm = data_adm
        self.cod_cargo = cod_cargo
        self.desc_cargo = desc_cargo
        self.sit_colab = sit_colab

class Registro_Folha_Pagamento():
    def __init__(self,matricula_colab, nome_colab, desc_cargo, desc_filial, desc_projeto, desc_conta_contabil,
                 cod_evento, desc_evento, proeventos, hora_min_ref, desc_sit_atual):
        self.matricula_colab = matricula_colab
        self.nome_colab = nome_colab
        self.desc_cargo = desc_cargo
        self.desc_filial = desc_filial
        self.desc_projeto = desc_projeto
        self.desc_conta_contabil = desc_conta_contabil
        self.cod_evento = cod_evento
        self.desc_evento = desc_evento
        self.proeventos = proeventos
        self.hora_min_ref = hora_min_ref
        self.desc_sit_atual = desc_sit_atual


class Registro_Provisao_Folha_Analitico_Colab():
    def __init__(self, periodo, cod_emp, nome_emp, cod_filial, nome_filial, cod_ccu, desc_ccu, handle_proj, mat_fun,
                nome_fun, cod_cargo, desc_cargo, data_adm, desc_prov, val_base_prov, perc_dias_prov, val_anterior_prov,
                val_transf_prov, val_ajuste_prov, val_prov, val_pag_prov, val_indenizado_prov, val_saldo_prov,
                tipo_provisao):
        self.periodo = periodo
        self.cod_emp = cod_emp
        self.nome_emp = nome_emp
        self.cod_filial = cod_filial
        self.nome_filial = nome_filial
        self.cod_ccu = cod_ccu
        self.desc_ccu = desc_ccu
        self.handle_proj = handle_proj
        self.mat_fun = mat_fun
        self.nome_fun = nome_fun
        self.cod_cargo = cod_cargo
        self.desc_cargo = desc_cargo
        self.data_adm = data_adm
        self.desc_prov = desc_prov
        self.val_base_prov = val_base_prov
        self.perc_dias_prov = perc_dias_prov
        self.val_anterior_prov = val_anterior_prov
        self.val_transf_prov = val_transf_prov
        self.val_ajuste_prov = val_ajuste_prov
        self.val_prov = val_prov
        self.val_pag_prov = val_pag_prov
        self.val_indenizado_prov = val_indenizado_prov
        self.val_saldo_prov = val_saldo_prov
        self.tipo_provisao = tipo_provisao


class Registro_Provisao_Folha_Analitico_Proevento():
    def __init__(self, desc_prov, val_base_prov,
                 perc_dias_prov, val_anterior_prov, val_transf_prov, val_ajuste_prov, val_prov, val_pag_prov,
                 val_indenizado_prov, val_saldo_prov, tipo_provisao):
        self.desc_prov = desc_prov
        self.val_base_prov = val_base_prov
        self.perc_dias_prov = perc_dias_prov
        self.val_anterior_prov = val_anterior_prov
        self.val_transf_prov = val_transf_prov
        self.val_ajuste_prov = val_ajuste_prov
        self.val_prov = val_prov
        self.val_pag_prov = val_pag_prov
        self.val_indenizado_prov = val_indenizado_prov
        self.val_saldo_prov = val_saldo_prov
        self.tipo_provisao = tipo_provisao

class Filial():
    def __init__(self, cod_empresa, nome_empresa, cod_filial, nome_filial):
        self.cod_empresa = cod_empresa
        self.nome_empresa = nome_empresa
        self.cod_filial = cod_filial
        self.nome_filial = nome_filial

class Ocorrencia_Jornada():
    def __init__(self, matricula, nome_colab, desc_cargo, desc_local, cod_filial, nome_filial, data_ocorr, jor_12h,
                 jor_15h, inter_jor):
        self.matricula = matricula
        self.nome_colab = nome_colab
        self.desc_cargo = desc_cargo
        self.desc_local = desc_local
        self.cod_filial = cod_filial
        self.nome_filial = nome_filial
        self.data_ocorr = data_ocorr
        self.jor_12h = jor_12h
        self.jor_15h = jor_15h
        self.inter_jor = inter_jor


class Empresa_Senior():
    def __init__(self, cod_empresa, nome_empresa):
        self.cod_empresa = cod_empresa
        self.nome_empresa = nome_empresa






