// Botão de Cadastro de Cargas , posterior envio para a View
$('#form_cadastro_sinistros_cargas').submit(function(event){
    event.preventDefault();
        // Coleta de dados cadastro de cargascb_tipo_frota_carga
    empresaSelecionada = document.getElementById("cb_empresa_sin_carga").value
    motoristaCargas = document.getElementById("txt_nome_motorista_carga").value
    dt_nascimento_motorista_carga = document.getElementById("dt_nascimento_motorista_carga").value
    tipoFrota = document.getElementById("cb_tipo_frota_carga").value//Seleção tipo de frota Agregado, Terceiro, Própria
    placaCarreta = document.getElementById("txt_placa_carreta_carga").value
    transportadorVeiculo = document.getElementById("txt_nome_transportador_dados_veiculo_carga").value
    placaVeiculo = document.getElementById("txt_placa_veiculo_carga").value
    projetoVeiculo = document.getElementById("cb_tipo_projeto_carga").value
    tipoVeiculo = document.getElementById("cb_tipo_veic_carga").value//Seleção tipo de veiculo baú, Graneleiro,
    placaCarreta = document.getElementById("txt_placa_carreta_carga").value
    clienteCarga = document.getElementById("txt_nome_cliente_carga").value
    numeroNotaCarga = document.getElementById("txt_numero_nota_carga").value
    valorProdutosCarga = document.getElementById("num_valor_dos_produtos_carga").value
    tipoProdutoCarga = document.getElementById("txt_tipo_mercadoria_carga").value
    numeroSerieCarga = document.getElementById("txt_numero_serie_carga").value
    dt_ocorrencia_sinistro_carga = document.getElementById("dt_ocorrencia_sinistro_carga").value
    sel_estado_sinistro_carga = document.getElementById("sel_estado_sinistro_carga").value
    localSinistro = document.getElementById("txt_local_sinistro_carga").value
    valorSinistro = document.getElementById("num_valor_sinistro_carga").value
    txt_cidade_sinistro_carga = document.getElementById("txt_cidade_sinistro_carga").value
    timeSinistro = document.getElementById("hr_sinistro_carga").value
    motivo_sinistro_carga = document.getElementById("cb_motivo_sinistro_carga").value
    respostaSeguro = document.getElementById("txt_resposta_seguro_sinistro_carga").value
    data_abertura_registro_sinistro = document.getElementById("dt_abertura_registro_sinistro_carga").value   //Abertura do registro de sinistros de cargas
    data_fechamento_registro_sinistro = document.getElementById("dt_encerramento_registro_sinistro_carga").value  //Encerramento do registro de sinistros de cargas
    seguradoraSinistro = document.getElementById("txt_seguradora_sinistro_carga").value
    reguladoraSinistro = document.getElementById("txt_reguladora_sinistro_carga").value
    feitoReembolso = document.getElementById("cb_feito_reembolso_sinistro_carga").value
    valorReembolso = document.getElementById("number_remboolso_registro_sinistro").value
    numeroProcesso = document.getElementById("txt_numero_dados_processo_sinistro_carga").value
    dt_abertura_processo_sinistro_carga = document.getElementById("dt_abertura_processo_sinistro_carga").value
    dt_fim_processo_sinistro_carga = document.getElementById("dt_fim_processo_sinistro_carga").value
    statusProcesso = document.getElementById("cb_status_processo_carga").value
    cod_cad_sinistro_carga = document.getElementById("btn_finalizar_cadastro_sinistro").value
    txt_obs_cad_carga = document.getElementById("txt_observacoes_finais_sinistro_carga").value


    // Envio dados para a View
    $.ajax({
        type: "POST",
        // Envia os dados pelo metodo POST para a URL
        url: "/cco_sinistro_app/cadastro_sinistros_cargas",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            empresaSelecionada : empresaSelecionada,
            motoristaCargas : motoristaCargas,
            dt_nascimento_motorista_carga : dt_nascimento_motorista_carga,
            tipoFrota : tipoFrota,
            transportadorVeiculo : transportadorVeiculo,
            placaVeiculo : placaVeiculo,
            projetoVeiculo : projetoVeiculo,
            tipoVeiculo : tipoVeiculo,
            placaCarreta : placaCarreta,
            clienteCarga : clienteCarga,
            numeroNotaCarga : numeroNotaCarga,
            valorProdutosCarga : valorProdutosCarga,
            tipoProdutoCarga : tipoProdutoCarga,
            numeroSerieCarga : numeroSerieCarga,
            dt_ocorrencia_sinistro_carga : dt_ocorrencia_sinistro_carga,
            sel_estado_sinistro_carga : sel_estado_sinistro_carga,
            localSinistro : localSinistro,
            valorSinistro : valorSinistro,
            txt_cidade_sinistro_carga : txt_cidade_sinistro_carga,
            timeSinistro : timeSinistro,
            motivo_sinistro_carga : motivo_sinistro_carga,
            respostaSeguro : respostaSeguro,
            data_abertura_registro_sinistro : data_abertura_registro_sinistro,
            data_fechamento_registro_sinistro : data_fechamento_registro_sinistro,
            seguradoraSinistro : seguradoraSinistro,
            reguladoraSinistro : reguladoraSinistro,
            feitoReembolso : feitoReembolso,
            valorReembolso : valorReembolso,
            numeroProcesso : numeroProcesso,
            dt_abertura_processo_sinistro_carga : dt_abertura_processo_sinistro_carga,
            dt_fim_processo_sinistro_carga : dt_fim_processo_sinistro_carga,
            statusProcesso : statusProcesso,
            txt_obs_cad_carga : txt_obs_cad_carga,
            cod_cad_sinistro_carga : cod_cad_sinistro_carga
        },
        success: function(data) {
            atualiza_cb_placa_pesq_sinistros_carga();
            $.gritter.add({
                title: 'Sucesso!',
                text: "Lançamento registrado com sucesso!",
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
        },
        error: function(error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

});
// Botão de Cadastro de equipamentos , posterior envio para a View
$('#form_cadastro_eqp_veiculos').submit(function(event){
    event.preventDefault();
        // Coleta de dados da form do cadastro de equipamentos e veiculos
        nome_motorista_eqp = document.getElementById("txt_nome_motorista_carga_cad_eqp").value //Nome motorista
        dt_nascimento_motorista_eqp = document.getElementById("dt_nascimento_motorista_eqp").value // Data Nascimento Motorista
        cpf_motorista_eqp = document.getElementById("cpf_motorista_eqp").value // Cpf Motorista
        projeto_eqp = document.getElementById("select_projeto_eqp").value //Projeto para cadastro
        placa_cavalo_cad_eqp = document.getElementById("txt_placa_cavalo_cad_eqp").value//Placa do Cavalo
        dt_ocorrencia_sinistro_carga_eqp = document.getElementById("dt_ocorrencia_sinistro_carga_eqp").value//Data ocorrencia sinistro Carga
        motivo_sinistro_eqp = document.getElementById("cb_motivo_sinistro_carga_eqp").value //Motivo Do sinistro
        acionado_seguro_eqp = document.getElementById("select_acionado_seg_eqp").value // Acionado Seguro, sim ou não
        cidade_sinistro_eqp = document.getElementById("cidade_sinistro_eqp").value //Cidade que ocorreu o sinistro
        estado_sinistro_eqp = document.getElementById("estado_sinistro_eqp").value //Estado que ocorreu o Sinistro
        dt_comunicacao_seguradora_eqp = document.getElementById("dt_comunicacao_seguradora_eqp").value //Data de comunicação a seguradora
        dt_comunicacao_cco_eqp = document.getElementById("dt_comunicacao_cco_eqp").value //data de comunicação ao CCO
        responsavel_dano_eqp = document.getElementById("txt_responsavel_por_dano_eqp").value //Responsável pelo dano
        desconto_colaborador_eqp = document.getElementById("cb_feito_desconto_colaborador_eqp").value //Desconto realizado ao colaborador
        indenizado_eqp = document.getElementById("select_indenizado_eqp").value //foi Indenizado ou não
        dano_empresa_eqp = document.getElementById("cb_houve_dano_aempresa_eqp").value //Houve danos a empresa sim ou não
        valor_indenizado_eqp = document.getElementById("value_indenizado_eqp").value // Valor indenizado
        valor_prejuizo_eqp = document.getElementById("value_prejuizo_eqp").value // Valor do prejuizo
        responsavel_pag_indenizacao_dano_eqp = document.getElementById("txt_responsavel_pag_indenizacao_dano_eqp").value // Responsável pela indenização do dano
        feito_reembolso_eqp = document.getElementById("txt_feito_reembolso_eqp_veic").value //Realizado Reembolso sim ou não
        tipo_acionamento_eqp = document.getElementById("cb_tipo_acionamento_eqp").value //Tipo de acionamento realizado
        numero_processo_eqp = document.getElementById("numero_processo_eqp").value //Numero do Processo
        dt_inicio_dados_processo_eqp = document.getElementById("dt_inicio_dados_processo_eqp").value //Data de inicio do processo
        dt_fim_processo_sinistro_carga_eqp = document.getElementById("dt_fim_processo_sinistro_carga_eqp").value //Data de fim do processo
        observacoes_finais = document.getElementById("observacoes_finais_eqp").value //Observações Finais do Cadastro
        status_processo_eqp = document.getElementById("status_processo_eqp").value
        cod_cad_sinistro_eqp_veic = document.getElementById("btn_finalizar_cadastro_sinistro_cad_eqp_veic").value //Defino valor inicial como 0 ao Button

    // Envio de dados para a view
            $.ajax({
            type: "POST",
            // Envia os dados pelo metodo POST para a URL
            url: "/cco_sinistro_app/cadastro_sinistros_eqp",
            data: {
                nome_motorista_eqp : nome_motorista_eqp,
                projeto_eqp : projeto_eqp,
                dt_nascimento_motorista_eqp : dt_nascimento_motorista_eqp,
                cpf_motorista_eqp : cpf_motorista_eqp,
                dt_ocorrencia_sinistro_carga_eqp : dt_ocorrencia_sinistro_carga_eqp,
                motivo_sinistro_eqp : motivo_sinistro_eqp,
                placa_cavalo_cad_eqp : placa_cavalo_cad_eqp,
                acionado_seguro_eqp : acionado_seguro_eqp,
                cidade_sinistro_eqp : cidade_sinistro_eqp,
                estado_sinistro_eqp : estado_sinistro_eqp,
                dt_comunicacao_seguradora_eqp : dt_comunicacao_seguradora_eqp,
                dt_comunicacao_cco_eqp : dt_comunicacao_cco_eqp,
                responsavel_dano_eqp : responsavel_dano_eqp,
                desconto_colaborador_eqp : desconto_colaborador_eqp,
                indenizado_eqp : indenizado_eqp,
                dano_empresa_eqp : dano_empresa_eqp,
                valor_indenizado_eqp : valor_indenizado_eqp,
                valor_prejuizo_eqp : valor_prejuizo_eqp,
                responsavel_pag_indenizacao_dano_eqp : responsavel_pag_indenizacao_dano_eqp,
                feito_reembolso_eqp : feito_reembolso_eqp,
                tipo_acionamento_eqp : tipo_acionamento_eqp,
                numero_processo_eqp : numero_processo_eqp,
                status_processo_eqp : status_processo_eqp,
                dt_inicio_dados_processo_eqp : dt_inicio_dados_processo_eqp,
                dt_fim_processo_sinistro_carga_eqp : dt_fim_processo_sinistro_carga_eqp,
                observacoes_finais : observacoes_finais,
                cod_cad_sinistro_eqp_veic : cod_cad_sinistro_eqp_veic
            },

            success: function(data) {
                atualiza_cb_placa_pesq_sinistros_carga();
                $.gritter.add({
                    title: 'Sucesso!',
                    text: "Lançamento registrado com sucesso!",
                    image: '/static/icons/sucess_icon.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
});
// Botão pesquisa de placa por competencia
$('#frm_pesq_sinistros_cargas_por_comp').submit(function(event){
        event.preventDefault();
        competencia_selecionada = document.getElementById('date_pesq_sinistro').value

        $.ajax({
            type: "GET",
            url: "/cco_sinistro_app/pesq_reg_sinistros",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                competencia_selecionada : competencia_selecionada,
                tipo_pesquisa_sinistro : 'data',

            },
            success: function(data) {
                              $.gritter.add({
                    title: 'Sucesso!',
                    text: "Pesquisa realizada com Sucesso!",
                    image: '/static/icons/sucess_icon.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });


});
// Estrutura de botões
$(document).on('click','button', function(){
    let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_limpar_campos_cargas"){
        document.getElementById("form_cadastro_sinistros_cargas").reset();
        $(window).scrollTop(0); // Rolando a página para o topo
        $("#cb_empresa_sin_carga").focus();
    }

    if (let_nome_btn == "btn_criar_form_eqp"){
        document.getElementById("form_cadastro_eqp_veiculos").reset();
        $(window).scrollTop(0); // Rolando a página para o topo
        $("#txt_nome_motorista_carga_cad_eqp").focus();
    }
    //Botão pesquisa por Placa
    else if(let_nome_btn == "btn_pesq_sinistros_carga"){
        atualiza_tab_pesq_sinistro('placa');
    }
    //Botão pesquisa por Data
    else if(let_nome_btn == "btn_pesq_sinistros_date"){
        atualiza_tab_pesq_sinistro('data');
    }
    //Botão excluir sinistro
    else if(let_nome_btn == "btn_excluir_sinistro"){
        let let_cod_btn_excluir_sinistro = let_val_btn;
        let let_tipo_pesquisa = $("#hd_tipo_pesquisa_sinistro").val();
        $.ajax({
                type: 'DELETE',
                url: '/cco_sinistro_app/exclui_registro_sinistro/'+let_cod_btn_excluir_sinistro,
                dataType: "json",
                success: function(data) {
                    atualiza_cb_placa_pesq_sinistros_carga();
                    atualiza_tab_pesq_sinistro(let_tipo_pesquisa);
                    $.gritter.add({
                        title: 'Sucesso!',
                        text: data.msg,
                        image: '/static/icons/sucess_icon.svg',
                        sticky: false,
                        time: '',
                    });
                },
                error: function (request, status, error) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });

    }
    //Botão Editar Sinistros
    else if(let_nome_btn == "btn_editar_sinistro"){
        let let_tipo_sinistro = let_val_btn.split("_")[0];
        let let_cod_sinistro =  let_val_btn.split("_")[1];
        $.ajax({
            type: "GET",
            url: "/cco_sinistro_app/edita_cadastro",
            data: {
                "tipo_sinistro":let_tipo_sinistro,
                "cod_sinistro":let_cod_sinistro,
            },
            success: function(dados) {
                if (let_tipo_sinistro == "C") {
                    $("#myTab a[href='#div_cadastro_sinistros_cargas']").tab("show");
                    // Aqui faço a coleta dos via jquery que foram tratados na minha view e encapsulados no dicionário.
                    // DADOS DO MOTORISTA
                    $("#cb_empresa_sin_carga").val(dados.dic_sinistro_form.empresa);
                    $("#cb_empresa_sin_carga").selectpicker('refresh');
                    $("#txt_nome_motorista_carga").val(dados.dic_sinistro_form.nome_mot);
                    $("#dt_nascimento_motorista_carga").val(dados.dic_sinistro_form.dat_nasc); //data nascimento motorista
                    $("#dt_nascimento_motorista_carga").selectpicker('refresh')
                    // DADOS DO VEICULO
                    $("#cb_tipo_frota_carga").val(dados.dic_sinistro_form.tipo_frota);
                    $("#cb_tipo_frota_carga").selectpicker('refresh');
                    $("#cb_tipo_veic_carga").val(dados.dic_sinistro_form.tipo_veiculo);
                    $("#cb_tipo_veic_carga").selectpicker('refresh');
                    $("#cb_tipo_projeto_carga").val(dados.dic_sinistro_form.cod_projeto);
                    $("#cb_tipo_projeto_carga").selectpicker('refresh');
                    $("#txt_placa_veiculo_carga").val(dados.dic_sinistro_form.placa_veiculo_cavalo);
                    $("#txt_placa_carreta_carga").val(dados.dic_sinistro_form.placa_veiculo_carreta);
                    $("#txt_nome_transportador_dados_veiculo_carga").val(dados.dic_sinistro_form.transportador);
                    // DADOS DA CARGA
                    $("#txt_nome_cliente_carga").val(dados.dic_sinistro_form.cliente);
                    $("#txt_numero_nota_carga").val(dados.dic_sinistro_form.nota_fiscal);
                    $("#num_valor_dos_produtos_carga").val(dados.dic_sinistro_form.valor_produtos);
                    $("#txt_tipo_mercadoria_carga").val(dados.dic_sinistro_form.tipo_mercadoria);
                    $("#txt_numero_serie_carga").val(dados.dic_sinistro_form.cte_serie);
                    // DADOS DO SINISTRO
                    $("#dt_ocorrencia_sinistro_carga").val(dados.dic_sinistro_form.data_ocorre_sinistro); //data ocorrência sinistro carga
                    $("#sel_estado_sinistro_carga").val(dados.dic_sinistro_form.cod_estado);
                    $("#sel_estado_sinistro_carga").selectpicker('refresh');
                    $("#txt_local_sinistro_carga").val(dados.dic_sinistro_form.local_Sinistro);
                    $("#num_valor_sinistro_carga").val(dados.dic_sinistro_form.valor_sinistro_carga);
                    $("#txt_cidade_sinistro_carga").val(dados.dic_sinistro_form.cidade);
                    $("#hr_sinistro_carga").val(dados.dic_sinistro_form.hora_sinistro);
                    $("#cb_motivo_sinistro_carga").val(dados.dic_sinistro_form.cod_motivo_sinistro);
                    $("#cb_motivo_sinistro_carga").selectpicker('refresh');
                    $("#txt_resposta_seguro_sinistro_carga").val(dados.dic_sinistro_form.resp_seguro);
                    // DADOS REGISTRO DO SINISTRO
                    $("#dt_abertura_registro_sinistro_carga").val(dados.dic_sinistro_form.data_abertura_registro_sinistro); //data de abertura do registro de sinistro
                    $("#txt_reguladora_sinistro_carga").val(dados.dic_sinistro_form.reguladora_sinistro);
                    $("#number_remboolso_registro_sinistro").val(dados.dic_sinistro_form.valor_reembolso);
                    $("#txt_seguradora_sinistro_carga").val(dados.dic_sinistro_form.seguradora);
                    $("#cb_feito_reembolso_sinistro_carga").val(dados.dic_sinistro_form.feito_reembolso);
                    $("#cb_feito_reembolso_sinistro_carga").selectpicker('refresh');
                    $("#dt_encerramento_registro_sinistro_carga").val(dados.dic_sinistro_form.data_fechamento_registro_sinistro); //data encerramento do registro de sinistro
                    // DADOS DO PROCESSO
                    $("#txt_numero_dados_processo_sinistro_carga").val(dados.dic_sinistro_form.num_processo);
                    $("#dt_abertura_processo_sinistro_carga").val(dados.dic_sinistro_form.data_abertura_processo);
                    $("#dt_fim_processo_sinistro_carga").val(dados.dic_sinistro_form.data_fechamento_processo);
                    // DOCUMENTAÇÃO E COMPLEMENTOS
                    $("#cb_status_processo_carga").val(dados.dic_sinistro_form.status_processo);
                    $("#cb_status_processo_carga").selectpicker('refresh');
                    $("#txt_observacoes_finais_sinistro_carga").val(dados.dic_sinistro_form.observacao);//Observações Finais cadastro de Cargas
                    $("#btn_finalizar_cadastro_sinistro").val(dados.dic_sinistro_form.cod_sinistro_carga);

                }

                else if (let_tipo_sinistro == "E") {
                    $("#myTab a[href='#div_tab_cad_sinistros_cad_eqp_veic']").tab("show");
                    // DADOS DO MOTORISTA
                    $("#txt_nome_motorista_carga_cad_eqp").val(dados.dic_sinistro_form.nome_mot);
                    $("#dt_nascimento_motorista_eqp").val(dados.dic_sinistro_form.data_nasc);
                    $("#cpf_motorista_eqp").val(dados.dic_sinistro_form.cpf_mot);
                    // DADOS DO VEICULO
                    $("#select_projeto_eqp").val(dados.dic_sinistro_form.cod_projeto);
                    $("#select_projeto_eqp").selectpicker('refresh');
                    $("#txt_placa_cavalo_cad_eqp").val(dados.dic_sinistro_form.placa_veiculo_cavalo);
                    // DADOS DO SINISTRO
                    $("#dt_ocorrencia_sinistro_carga_eqp").val(dados.dic_sinistro_form.data_ocorre_sinistro);
                    $("#cb_motivo_sinistro_carga_eqp").val(dados.dic_sinistro_form.cod_motivo_sinistro);
                    $("#cb_motivo_sinistro_carga_eqp").selectpicker('refresh');
                    $("#select_acionado_seg_eqp").val(dados.dic_sinistro_form.acionado_seguro);
                    $("#select_acionado_seg_eqp").selectpicker('refresh');
                    $("#cidade_sinistro_eqp").val(dados.dic_sinistro_form.cidade);
                    $("#estado_sinistro_eqp").val(dados.dic_sinistro_form.cod_estado);
                    $("#estado_sinistro_eqp").selectpicker('refresh');
                    // COMUNICAÇÃO SINISTRO
                    $("#dt_comunicacao_seguradora_eqp").val(dados.dic_sinistro_form.data_comunicacao_seguradora);
                    $("#dt_comunicacao_cco_eqp").val(dados.dic_sinistro_form.data_comunicacao_cco);
                    // INFORMAÇÕES ADICIONAIS
                    $("#txt_responsavel_por_dano_eqp").val(dados.dic_sinistro_form.resp_dano);
                    $("#txt_responsavel_por_dano_eqp").selectpicker('refresh');
                    $("#cb_feito_desconto_colaborador_eqp").val(dados.dic_sinistro_form.descontado_colab);
                    $("#cb_feito_desconto_colaborador_eqp").selectpicker('refresh');
                    $("#select_indenizado_eqp").val(dados.dic_sinistro_form.indenizado);
                    $("#select_indenizado_eqp").selectpicker('refresh');
                    $("#cb_houve_dano_aempresa_eqp").val(dados.dic_sinistro_form.houve_danos_emp);
                    $("#cb_houve_dano_aempresa_eqp").selectpicker('refresh');
                    $("#value_indenizado_eqp").val(dados.dic_sinistro_form.val_indenizado);
                    $("#value_prejuizo_eqp").val(dados.dic_sinistro_form.val_prejuizo);
                    $("#txt_responsavel_pag_indenizacao_dano_eqp").val(dados.dic_sinistro_form.resp_indenizar_dano);
                    $("#txt_responsavel_pag_indenizacao_dano_eqp").selectpicker('refresh');
                    $("#txt_feito_reembolso_eqp_veic").val(dados.dic_sinistro_form.feito_reembolso_eqp);
                    $("#txt_feito_reembolso_eqp_veic").selectpicker('refresh');
                    // DADOS DO PROCESSO
                    $("#cb_tipo_acionamento_eqp").val(dados.dic_sinistro_form.tipo_acionamento);
                    $("#cb_tipo_acionamento_eqp").selectpicker('refresh');
                    $("#numero_processo_eqp").val(dados.dic_sinistro_form.num_processo);
                    $("#dt_inicio_dados_processo_eqp").val(dados.dic_sinistro_form.data_inicio_processo);
                    $("#dt_fim_processo_sinistro_carga_eqp").val(dados.dic_sinistro_form.data_fim_processo);
                    $("#observacoes_finais_eqp").val(dados.dic_sinistro_form.observacao);//Observações finais cadastro de Equipamentos
                    $("#btn_finalizar_cadastro_sinistro_cad_eqp_veic").val(dados.dic_sinistro_form.cod_sinistro_eqp_veic);
                }

            },
            error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });

    }
});
// Após cadastro de carga atualiza as placas da pesquisa
function atualiza_cb_placa_pesq_sinistros_carga (){
    $("#cb_placa_pesq_sinistros_carga option").remove();
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/cco_sinistro_app/atualiza_cb_placa_pesq_sinistros_carga",
        success: function(dados){
            dados.lista_placas.forEach(placa => {
                $("#cb_placa_pesq_sinistros_carga").append("<option value='"+
                placa.placa_veiculo_cavalo+"'>"+placa.placa_veiculo_cavalo+"</option>");

            });
            $("#cb_placa_pesq_sinistros_carga").selectpicker('refresh');
        },
        error: function(request, status, error){
            $.gritter.add({
                title: 'Por gentileza contate o adm.',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        },
    });
};
//Atualiza Tabela sinistros por competencia e placa
function atualiza_tab_pesq_sinistro (tipo_pesquisa){
    dados_parametros = ''
    if( tipo_pesquisa == 'placa'){
        placa_selecionada = $("#cb_placa_pesq_sinistros_carga").val();
        dados_parametros = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            placa_selecionada : placa_selecionada,
            tipo_pesquisa_sinistro : tipo_pesquisa
        }
    } else if(tipo_pesquisa == 'data'){
        competencia_selecionada = $("#competencia_selecionada").val()
        // Divide o valor em ano e mês
        var partes = competencia_selecionada.split("-");
        // Obtém o ano e o mês
        var ano = partes[0];
        var mes = partes[1] - 1; // Subtrai 1 para obter o mês correto (0 a 11)
        // Constrói a data de início da competência
        var inicioCompetencia = new Date(ano, mes, 1).toISOString().substring(0, 10); // Primeiro dia do mês
        var ultimoDia = new Date(ano, mes + 1, 0).getDate();
        var fimCompetencia = new Date(ano, mes, ultimoDia).toISOString().substring(0, 10); // Último dia do mês
        dados_parametros = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            inicioCompetencia : inicioCompetencia,
            fimCompetencia : fimCompetencia,
            tipo_pesquisa_sinistro : tipo_pesquisa
        }
    }
    $.ajax({
        type: "GET",
        url: "/cco_sinistro_app/pesq_reg_sinistros",
        data: dados_parametros,
        success: function(data) {
            $("#hd_tipo_pesquisa_sinistro").val(tipo_pesquisa);
            const consulta_sinistros = data.linhasTabela.map(linha => [
                linha.tipo_sinistro == "C" ? 'Carga' : (linha.tipo_sinistro == "E" ? 'Equip e Veic' : ''),
                linha.nome_mot,
                linha.cpf_mot,
                formatarData(linha.data_nasc),
                linha.desc_projeto,
                linha.placa_veiculo_cavalo,
                formatarData(linha.data_ocorre_sinistro),
                linha.desc_motivo_sinistro,
                linha.acionado_seguro =="S" ? 'Sim' : (linha.tipo_sinistro == "N" ? 'Não' : ''),
                linha.num_processo,
                `
                <button type='button' id="btn_editar_sinistro_${linha.cod_sinistro} "
                    name="btn_editar_sinistro"
                    class="btn btn-primary btn-rounded btn-editar"
                    value="${linha.tipo_sinistro}_${linha.cod_sinistro}"
                    title="Editar sinistro">
                    <i class="fa-solid fa-pen-to-square"></i>
                </button>
                ` ,
                `
                <button type='button' id="btn_excluir_sinistro_${linha.cod_sinistro} "
                    name="btn_excluir_sinistro"
                    class="btn btn-primary btn-rounded btn-excluir"
                    value="${linha.cod_sinistro}"
                    title="Excluir sinistro">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
                `
            ])

            $('#table_sinistros_cargas').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":consulta_sinistros,
                "columns": [
                    { title: "Tipo Sinistro" },
                    { title: "Motorista" },
                    { title: "CPF" },
                    { title: "Dt.Nascimento" },
                    { title: "Projeto" },
                    { title: "Placa" },
                    { title: "Dt.Sinistro" },
                    { title: "Motivo do Sinistro" },
                    { title: "Seguro" },
                    { title: "Nº Processo" },
                    { title: "Editar" },
                    { title: "Excluir" },
                ],
                "columnDefs": [{
                    // { "width": "10%", "targets": 0 },
                    // {"className": "dt-left", "targets": [0]},
                    // {"className": "dt-left", "targets": [1]}
                }
                ],
                "oLanguage": {
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "Mostrar MENU registros",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "Mostrando de START até END de TOTAL registros",
                    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "Primeiro",
                        "sPrevious": "Anterior",
                        "sNext":     "Proximo",
                        "sLast":     "Último"
                    },
                    "buttons":{
                        "copyTitle": 'Dados Copiados',
                        "copySuccess": {
                            _: '%d linhas copiadas',
                            1: '1 linha copiada'
                        }
                    }
                }
            });
            $.gritter.add({
                title: 'Sucesso!',
                text: "Pesquisa realizada com Sucesso!",
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
        },
        error: function(error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
		}
	});

};
// Função para formatar a data no formato "dia mês e ano"
function formatarData(data) {
    if(data){
        const partesData = data.split('-'); // Divide a data em partes (ano, mês, dia)
        const dataFormatada = `${partesData[2]}/${partesData[1]}/${partesData[0]}`; // Formato: dia/mês/ano
        return dataFormatada;
    }
    else {
        return null;
    }
};
// Função para formatar campo de entrada de Placa de cavalo e carreta
function formatarPlaca(input) {
    let placa = input.value.replace(/[^a-zA-Z0-9]/g, '');

    let letras = placa.substring(0, 3).replace(/[^a-zA-Z]/g, '');
    let numeros = placa.substring(3, 8).replace(/[^0-9]/g, '');

    placa = letras.toUpperCase() + '-' + numeros;

    input.value = placa;
}
//Modal Código de erro
function mostrarPopup() {
    $('#msg_erro_cod').modal('show');
}
