

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).on('click', 'button', function(){
    let let_cor_empresa = $("#hd_cor_empresa_frm_custos_placa").val();
	let let_nome_btn = $(this).attr('name');
	let let_id_btn = $(this).attr('id');
	let let_val_btn = $(this).val();

    if (let_nome_btn == 'btn_desmarcar_projetos_frm_custos_placa'){
        $("#sl_proj_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_proj_frm_custos_placa') {
        $("#sl_proj_custos_placa").selectpicker('selectAll');
    } else if (let_nome_btn == 'btn_desmarcar_tipo_veic_equip_frm_custos_placa'){
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_tipo_veic_equip_frm_custos_placa') {
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('selectAll');
    } else if ( let_nome_btn == 'btn_gera_dados_custos_placas_proj' ) {
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_lista_handle_contas = $("#sl_conta_frm_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_filial_projeto_placa',
                'handle_filial'         :   let_handle_filial,
                'lista_handle_contas'   :   let_lista_handle_contas,
                'comp'                  :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){

                let let_dv_total_filial = `
                    <div class="d-flex justify-content-between align-items-between w-100 p-2">
                        <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                            <span style="font-size: 16px;font-weight: 400;">&nbsp;&nbsp;</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">R$ Orçado</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">R$ Remunerado</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">R$ Realizado</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">% Realizado</span>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                        <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                            <span style="font-size: 16px;font-weight: 400;">TOTAL FILIAL</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">${dados.total_orc_filial}</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">${dados.total_rem_filial}</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">${dados.total_real_filial}</span>
                        </div>
                        <div class="d-flex flex-column justify-content-center align-items-center p-2" style="width: 15%;">
                            <span style="font-size: 16px;font-weight: 400;">100%</span>
                        </div>
                    </div>
                `;
                $("#dv_total_filial").html(let_dv_total_filial);


                let let_conteudo_div_tab_resumo_custos_fil = gera_estrutura_custos_filial(dados.dic_resumo_filial, dados.total_real_filial, dados.total_orc_filial, dados.total_rem_filial);
                $("#div_tab_resumo_custos_fil").html(let_conteudo_div_tab_resumo_custos_fil);


                let let_conteudo_div_tab_resumo_custos_proj = gera_estrutura_custos_projeto(dados.dic_resumo_projeto);
                $("#div_tab_resumo_custos_proj").html(let_conteudo_div_tab_resumo_custos_proj);

                let let_conteudo_div_tab_resumo_custos_placa = gera_estrutura_custos_placas(dados.dic_resumo_placas);
                $("#div_tab_resumo_custos_placa").html(let_conteudo_div_tab_resumo_custos_placa);

                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    } else if (let_nome_btn == 'btn_desmarcar_conta_frm_custos_placa'){
        $("#sl_conta_frm_custos_placa").selectpicker('deselectAll');

    }
    else if (let_nome_btn == 'btn_seleciona_todas_conta_frm_custos_placa') {
        $("#sl_conta_frm_custos_placa").selectpicker('selectAll');
    } else if(let_nome_btn == 'btn_abri_modal_lista_os_razao_conta') {

        $("#tab_lista_os_razao_placa tbody tr").remove();
        let let_cod_razao_frota = $(this).val();
        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        let let_cor_empresa = $("#hd_cor_empresa_frm_custos_placa").val();
        $.ajax({
            type: 'GET',
            data: {
                'cod_razao_frota'         :   let_cod_razao_frota
            },
            url:"/frota_custos_placa_app/retorna_oss_razao_conta",
            success: function(dados){
                let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: ${let_cor_empresa}"></i>
                `;

                let div_os = `

                `;
                dados.lista_obj_os_razao_conta.forEach(os => {
                    let let_checked = '';
                    if (os.eh_cluster == 1) {
                        let_checked = ' checked ';
                    }

                    let let_input_cluster_check = `
                        <input type="checkbox" ${let_checked} id="ck_os_razao_conta_${os.cod_os_razao_frota}"
                            name="ck_os_razao_conta">
                    `;

                    let let_obs_os = `&nbsp;&nbsp;`;
                    if( os.obs_os != null && os.obs_os != ''){
                        let_obs_os = os.obs_os;
                    }

                    let let_fornecedor = `&nbsp;&nbsp;`;
                    if( os.cod_razao_frota__nome_fornecedor != null ){
                        let_fornecedor = os.cod_razao_frota__nome_fornecedor;
                    }

                    div_os += `
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>${let_img}&nbsp;&nbsp;OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_os}</div>
                            </div>
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Tipo OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_tipo_os}</div>
                            </div>
                            <div class="d-flex flex-column w-100 justify-content-center align-items-end" style="margin-right: 0.25rem;">
                                ${let_input_cluster_check}
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Item</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_prod}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Qtd.</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.qtd_prod}</div>
                            </div>
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Conjunto</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_conj}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Observação OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                      style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${let_obs_os}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div><i class="fa-solid fa-receipt"></i>&nbsp;&nbsp;Núm. Contábil</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__doc_contabil}</div>
                            </div>
                            <div class="d-flex flex-column w-100 align-items-start" style="margin-right: 0.25rem;">
                                <div>Tipo Conta</div>
                                <div class="d-flex justify-content-end align-items-center w-100 p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__desc_tipo_conta}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Fornecedor</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${let_fornecedor}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Histórico lançamento</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__historico}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Projeto</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__desc_projeto}</div>
                            </div>
                        </div>
                    `;
                });
                div_os += `
                    </div>
                `;

                let_loader_frm_custos_placa.style.display = "none";
                $("#div_dados_os").html(div_os);
                $("#modal_lista_os_razao_conta").show();


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });

    } else if(let_nome_btn == 'bnt_custo_frota_proj'){
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_lista_handle_contas = $("#sl_conta_frm_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();
        let let_handle_proj = let_val_btn;

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_projeto_contas',
                'handle_filial'         :   let_handle_filial,
                'lista_handle_contas'   :   let_lista_handle_contas,
                'comp'                  :   let_comp,
                'handle_proj'           :   let_handle_proj
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){


                let let_contleudo_custos_proj_contas = gera_estrutura_custos_projeto_contas(dados.dic_resumo_projeto_contas, let_handle_proj);
                $("#div_dados_proj_contas_"+let_handle_proj).html(let_contleudo_custos_proj_contas);
                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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
    else if(let_nome_btn == 'bnt_custo_frota_fil_conta'){
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_handle_conta = let_val_btn;
        let let_comp = $("#dt_comp_frm_custos_placa").val();
        let let_handle_proj = let_val_btn;

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_fil_conta_projetos',
                'handle_filial'         :   let_handle_filial,
                'handle_conta'         :   let_handle_conta,
                'comp'                  :   let_comp,
                'handle_proj'           :   let_handle_proj
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){


                let let_contleudo_custos_proj_contas = gera_estrutura_custos_filial_conta_projetos(dados.dic_resumo_projetos, let_handle_conta);
                $("#div_dados_fil_contas_projetos_"+let_handle_proj).html(let_contleudo_custos_proj_contas);
                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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
    else if(let_nome_btn == 'bnt_custo_frota_fil_conta_proj'){
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_handle_conta = let_val_btn.split('_')[0];
        let let_comp = $("#dt_comp_frm_custos_placa").val();
        let let_handle_proj = let_val_btn.split('_')[1];

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_fil_conta_projeto_placas',
                'handle_filial'         :   let_handle_filial,
                'handle_conta'         :   let_handle_conta,
                'comp'                  :   let_comp,
                'handle_proj'           :   let_handle_proj
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){


                let let_contleudo_custos_conta_proj_placas = gera_estrutura_custos_filial_conta_projeto_placas(dados.dic_resumo_placas);
                $("#div_dados_fil_contas_proj_placas_"+let_handle_proj).html(let_contleudo_custos_conta_proj_placas);
                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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
    else if(let_nome_btn == 'bnt_custo_frota_proj_conta'){
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_handle_conta = let_val_btn.split('_')[0];
        let let_comp = $("#dt_comp_frm_custos_placa").val();
        let let_handle_proj = let_val_btn.split('_')[1];

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_proj_conta_placas',
                'handle_filial'         :   let_handle_filial,
                'handle_conta'         :   let_handle_conta,
                'comp'                  :   let_comp,
                'handle_proj'           :   let_handle_proj
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){


                let let_contleudo_custos_proj_conta_placas = gera_estrutura_custos_proj_conta_placas(dados.dic_resumo_placas);
                $("#div_dados_custo_proj_conta_placas_"+let_handle_conta).html(let_contleudo_custos_proj_conta_placas);
                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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
    else if(let_nome_btn == 'bnt_custo_frota_placa'){
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_lista_handle_contas = $("#sl_conta_frm_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();
        let let_placa = let_val_btn;

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_placas_contas',
                'handle_filial'         :   let_handle_filial,
                'lista_handle_contas'   :   let_lista_handle_contas,
                'comp'                  :   let_comp,
                'placa'                 :   let_placa
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){


                let let_contleudo_custos_placa_contas = gera_estrutura_custos_placa_contas(dados.dic_resumo_contas);
                $("#div_dados_placa_contas_"+let_placa).html(let_contleudo_custos_placa_contas);
                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });


    } else if(let_nome_btn == 'btn_razao_filial_conta_proj_placa' || let_nome_btn == 'btn_detalhes_lanc_proj_conta_placa'){
        $("#accordion_razao_custos_frota").html("");
        let let_handle_filial = let_val_btn.split('_')[0];
        let let_handle_conta = let_val_btn.split('_')[1];
        let let_handle_proj = let_val_btn.split('_')[2];
        let let_placa = let_val_btn.split('_')[3];
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_razao_filial_conta_proj_placa',
                'handle_filial'         :   let_handle_filial,
                'handle_proj'           :   let_handle_proj,
                'handle_conta'          :   let_handle_conta,
                'comp'                  :   let_comp,
                'placa'                 :   let_placa
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                let let_header = `Razão placa ${let_placa}. `;
                $("#sp_header_modal_razao_placa").html(let_header);

                let let_conteudo_razao = gera_estrutura_razao_filial_conta_proj_placa(dados.dic_resumo_razao);
                $("#accordion_razao_custos_frota").html(let_conteudo_razao);
                $("#modal_lista_razao_os_conta").show();
                let_loader_frm_custos_placa.style.display = "none";

                $("#modal_lista_razao_os_conta").show();

            },
            error: function (request, status, error) {
                console.log(error);
                let_loader_frm_custos_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });

    } else if(let_nome_btn == 'btn_fecha_modal_lista_razao_os_conta'){
        $("#modal_lista_razao_os_conta").hide();

    } else if(let_nome_btn == 'btn_detalhes_lanc_placa_conta'){
        $("#accordion_razao_custos_frota").html("");
        let let_handle_filial = let_val_btn.split('_')[0];
        let let_handle_conta = let_val_btn.split('_')[1];
        let let_placa = let_val_btn.split('_')[3];
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'transacao'             :   'pesquisa_razao_filial_placa_conta',
                'handle_filial'         :   let_handle_filial,
                'handle_conta'          :   let_handle_conta,
                'comp'                  :   let_comp,
                'placa'                 :   let_placa
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                let let_header = `Razão placa ${let_placa}. `;
                $("#sp_header_modal_razao_placa").html(let_header);

                let let_conteudo_razao = gera_estrutura_razao_filial_conta_proj_placa(dados.dic_resumo_razao);
                $("#accordion_razao_custos_frota").html(let_conteudo_razao);
                $("#modal_lista_razao_os_conta").show();
                let_loader_frm_custos_placa.style.display = "none";

                $("#modal_lista_razao_os_conta").show();

            },
            error: function (request, status, error) {
                console.log(error);
                let_loader_frm_custos_placa.style.display = "none";
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

});



$(document).on('change','#sl_cluster_frm_custos_placa', function(){
    let let_nome_select = $(this).attr('name');
    let let_id_select = $(this).attr('id');

    let let_cod_razao_frota = let_id_select.split('_')[5];
    let let_cod_item_cluster = $(this).val();

    let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
    let_loader_frm_custos_placa.style.display = "flex";
    $.ajax({
        type: 'POST',
        url: '/frota_custos_placa_app/altera_item_cluster_lancamento',
        data: {
            'cod_razao_frota'   :   let_cod_razao_frota,
            'cod_item_cluster'  :   let_cod_item_cluster
        },
        dataType: 'json',
        success: function (dados) {
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });



            let_loader_frm_custos_placa.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_custos_placa.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
      }
    });

});

$(document).on('change','input', function(){
    let let_name_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');

    if(let_name_input == 'ck_os_razao_conta'){
        let let_cod_os_razao_conta = let_id_input.split('_')[4];
        let let_check_comp = $(this).prop("checked");
        let let_status_check_comp = 0;
        if (let_check_comp == true) {
            let_status_check_comp = 1;
        }
        $.ajax({
            type: "POST",
            url: '/frota_custos_placa_app/altera_status_cluster_razao',
            data: {
                'cod_os_razao_conta'       :   let_cod_os_razao_conta,
                'status_check_comp'        :   let_status_check_comp
            },
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
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

});


$(document).on('change','#sl_handle_filial_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#sl_tipo_veic_equip_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#dt_comp_frm_custos_placa', function(){
    atualiza_componente_sl_conta();
});

function atualiza_componente_sl_conta(){
    let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
    //let let_lista_handle_tipo_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
    let let_comp = $("#dt_comp_frm_custos_placa").val();

    if( let_handle_filial != '' && let_comp != null && let_comp != '') {
        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'handle_filial'         :   let_handle_filial,
                //'lista_handle_tipo_contas'  :   let_lista_handle_tipo_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/atualiza_comp_sl_contas",
            success: function(dados){

                $("#sl_conta_frm_custos_placa option").remove();
                dados.lista_contas_periodo.forEach(conta => {
                    $("#sl_conta_frm_custos_placa").append(`<option value="${conta.handle_conta}">${conta.desc_conta}</option>`);
                });
                $("#sl_conta_frm_custos_placa").prop('disabled', false);
                $("#sl_conta_frm_custos_placa").selectpicker('refresh');

                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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



}

/* Inicio funções Aba Resumo Filial */
function gera_estrutura_custos_filial(dic_resumo_filial, total_real_filial, total_orc_filial, total_rem_filial){

    let let_conteudo_div_tab_resumo_custos_fil = `<div class="accordion" id="accordion_fil">`;
    dic_resumo_filial.forEach(conta => {
        let_conteudo_div_tab_resumo_custos_fil += `

            <div class="accordion-item">
                <h6 class="accordion-header" id="heading_fil_conta_${conta.HANDLE_CONTA}">
                    <button id="bnt_custo_frota_fil_conta_${conta.HANDLE_CONTA}" name="bnt_custo_frota_fil_conta"
                            value="${conta.HANDLE_CONTA}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_fil_conta_${conta.HANDLE_CONTA}" aria-expanded="false"
                            aria-controls="collapse_fil_conta_${conta.HANDLE_CONTA}" style="font-size:12px;">



                        <div class="d-flex justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                                <span style="font-size: 12px; font-weight: 600;">
                                    <i class="fa-solid fa-bookmark icon-color-e"></i>&nbsp;&nbsp;
                                    ${conta.NOME_CONTA}
                                </span>
                            </div>

                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${conta.VAL_LANC}</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${conta.perc_realizado}%</span>
                            </div>
                        </div>
                    </button>
                </h6>
                <div id="collapse_fil_conta_${conta.HANDLE_CONTA}" class="accordion-collapse collapse"
                     aria-labelledby="heading_fil_conta_${conta.HANDLE_CONTA}" data-bs-parent="#accordion_docs">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_fil_contas_projetos_${conta.HANDLE_CONTA}">


                    </div>
                </div>
            </div>
        `;
    });
    let_conteudo_div_tab_resumo_custos_fil += `</div>`;
    return let_conteudo_div_tab_resumo_custos_fil;
}

function gera_estrutura_custos_filial_conta_projetos(dic_resumo_proj, handle_conta){

    let let_conteudo_div_tab_resumo_custos_fil_conta_projetos = ``;
    let_conteudo_div_tab_resumo_custos_fil_conta_projetos += `
        <div class="accordion" id="accordion_fil_conta_proj">
    `;
    dic_resumo_proj.forEach(proj => {
        let_conteudo_div_tab_resumo_custos_fil_conta_projetos += `

            <div class="accordion-item">
                <h6 class="accordion-header" id="heading_fil_conta_proj${proj.HANDLE_PROJETO}">
                    <button id="bnt_custo_frota_fil_conta_proj_${proj.HANDLE_PROJETO}" name="bnt_custo_frota_fil_conta_proj"
                            value="${handle_conta}_${proj.HANDLE_PROJETO}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_fil_conta_proj_${proj.HANDLE_PROJETO}" aria-expanded="false"
                            aria-controls="collapse_fil_conta_proj_${proj.HANDLE_PROJETO}" style="font-size:12px;">



                        <div class="d-flex justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                                <span style="font-size: 12px; font-weight: 600;">
                                    <i class="fa-solid fa-caret-right"></i>&nbsp;&nbsp;
                                    ${proj.NOME_PROJETO}
                                </span>
                            </div>

                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${proj.VAL_LANC}</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${proj.perc_realizado}%</span>
                            </div>
                        </div>
                    </button>
                </h6>
                <div id="collapse_fil_conta_proj_${proj.HANDLE_PROJETO}" class="accordion-collapse collapse"
                     aria-labelledby="heading_fil_conta_proj_${proj.HANDLE_PROJETO}" data-bs-parent="#accordion_docs">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_fil_contas_proj_placas_${proj.HANDLE_PROJETO}">


                    </div>
                </div>
            </div>
        `;
    });
    let_conteudo_div_tab_resumo_custos_fil_conta_projetos += `</div>`;
    return let_conteudo_div_tab_resumo_custos_fil_conta_projetos;
}

function gera_estrutura_custos_filial_conta_projeto_placas(dic_resumo_placas){

    let let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas = ``;

    dic_resumo_placas.forEach(placa => {
        let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas += `

            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                    <span style="font-size: 12px; font-weight: 600;">
                        <button type='button'
                                name="btn_razao_filial_conta_proj_placa"
                                id="btn_razao_filial_conta_proj_placa_${placa.PLACA}"
                                class="btn btn-rounded btn-space"
                                value=${placa.handle_filial}_${placa.HANDLE_CONTA}_${placa.HANDLE_PROJETO}_${placa.PLACA}>
                            <i class="fa-solid fa-eye icon-color-e"></i>
                            ${placa.PLACA}
                        </button>

                    </span>
                </div>

                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${placa.VAL_LANC}</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${placa.perc_realizado}%</span>
                </div>
            </div>
        `;
    });
    return let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas;
}


/* Fim funções Aba Resumo Filial */

/* Inicio funções Aba Resumo Projeto */
function gera_estrutura_custos_projeto(dic_resumo_projeto){
    let let_conteudo_div_tab_resumo_custos_proj = `<div class="accordion" id="accordion_proj">`;

    dic_resumo_projeto.forEach(proj => {
        let_conteudo_div_tab_resumo_custos_proj += `

            <div class="accordion-item">
                <h6 class="accordion-header" id="heading_${proj.HANDLE_PROJETO}">
                    <button id="bnt_custo_frota_proj_${proj.HANDLE_PROJETO}" name="bnt_custo_frota_proj"
                            value="${proj.HANDLE_PROJETO}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_${proj.HANDLE_PROJETO}" aria-expanded="false"
                            aria-controls="collapse_${proj.HANDLE_PROJETO}" style="font-size:12px;">
                        <div class="d-flex justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                                <span style="font-size: 12px; font-weight: 600;">
                                    <i class="fa-solid fa-bookmark icon-color-e"></i>&nbsp;&nbsp;
                                    ${proj.NOME_PROJETO}
                                </span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${proj.VAL_LANC}</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${proj.perc_realizado}%</span>
                            </div>
                        </div>
                    </button>
                </h6>
                <div id="collapse_${proj.HANDLE_PROJETO}" class="accordion-collapse collapse"
                     aria-labelledby="heading_${proj.HANDLE_PROJETO}" data-bs-parent="#accordion_docs">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_proj_contas_${proj.HANDLE_PROJETO}">


                    </div>
                </div>
            </div>
        `;
    });
    let_conteudo_div_tab_resumo_custos_proj += `</div>`;
    return let_conteudo_div_tab_resumo_custos_proj;
}

function gera_estrutura_custos_projeto_contas(dic_resumo_projeto_contas, handle_proj){
    let let_conteudo_div_tab_resumo_custos_proj_conta = `
        <div class="accordion" id="accordion_conta">
    `;
    dic_resumo_projeto_contas.forEach(conta => {
        let_conteudo_div_tab_resumo_custos_proj_conta += `

            <div class="accordion-item">
                <h6 class="accordion-header" id="heading_conta_${conta.HANDLE_CONTA}">
                    <button id="bnt_custo_frota_proj_conta_${conta.HANDLE_CONTA}" name="bnt_custo_frota_proj_conta"
                            value="${conta.HANDLE_CONTA}_${handle_proj}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_conta_${conta.HANDLE_CONTA}" aria-expanded="false"
                            aria-controls="collapse_conta_${conta.HANDLE_CONTA}" style="font-size:12px;">
                        <div class="d-flex justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                                <span style="font-size: 12px; font-weight: 600;">
                                    <i class="fa-solid fa-caret-right"></i>&nbsp;&nbsp;
                                    ${conta.NOME_CONTA}
                                </span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${conta.VAL_LANC}</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${conta.perc_realizado}%</span>
                            </div>
                        </div>
                    </button>
                </h6>
                <div id="collapse_conta_${conta.HANDLE_CONTA}" class="accordion-collapse collapse"
                     aria-labelledby="heading_conta_${conta.HANDLE_CONTA}" data-bs-parent="#accordion_docs">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_custo_proj_conta_placas_${conta.HANDLE_CONTA}">


                    </div>
                </div>
            </div>
        `;
    });
    let_conteudo_div_tab_resumo_custos_proj_conta += `</div>`;
    return let_conteudo_div_tab_resumo_custos_proj_conta;
}

function gera_estrutura_custos_proj_conta_placas(dic_resumo_placas){

    let let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas = ``;
    dic_resumo_placas.forEach(placa => {
        let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas += `

            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                    <span style="font-size: 12px; font-weight: 600;">
                        <button type='button'
                                name="btn_detalhes_lanc_proj_conta_placa"
                                id="btn_detalhes_lanc_proj_conta_placa_${placa.PLACA}"
                                class="btn btn-rounded btn-space"
                                value=${placa.handle_filial}_${placa.HANDLE_CONTA}_${placa.HANDLE_PROJETO}_${placa.PLACA}>
                            <i class="fa-solid fa-eye icon-color-e"></i>
                            ${placa.PLACA}
                        </button>
                    </span>
                </div>

                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${placa.VAL_LANC}</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${placa.perc_realizado}%</span>
                </div>
            </div>
        `;
    });
    return let_conteudo_div_tab_resumo_custos_fil_conta_projeto_placas;
}

/* Fim funções Aba Resumo Projeto */

/* Início funções Aba Resumo Placa */
function gera_estrutura_custos_placas(dic_resumo_placas){

    let let_conteudo_div_tab_resumo_custos_placa = `<div class="accordion" id="accordion_placas">`;

    dic_resumo_placas.forEach(placa => {
        let_conteudo_div_tab_resumo_custos_placa += `

            <div class="accordion-item">
                <h6 class="accordion-header" id="heading_placa_${placa.PLACA}">
                    <button id="bnt_custo_frota_placa_${placa.PLACA}" name="bnt_custo_frota_placa"
                            value="${placa.PLACA}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_placa_${placa.PLACA}" aria-expanded="false"
                            aria-controls="collapse_placa_${placa.PLACA}" style="font-size:12px;">



                        <div class="d-flex justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                                <span style="font-size: 12px; font-weight: 600;">
                                    <i class="fa-solid fa-bookmark icon-color-e"></i>&nbsp;&nbsp;
                                    ${placa.PLACA}
                                </span>
                            </div>

                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">0,00</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${placa.VAL_LANC}</span>
                            </div>
                            <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                                <span style="font-size: 12px;font-weight: 600;">${placa.perc_realizado}%</span>
                            </div>
                        </div>
                    </button>
                </h6>
                <div id="collapse_placa_${placa.PLACA}" class="accordion-collapse collapse"
                     aria-labelledby="heading_placa_${placa.PLACA}" data-bs-parent="#accordion_docs">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_placa_contas_${placa.PLACA}">


                    </div>
                </div>
            </div>
        `;
    });
    let_conteudo_div_tab_resumo_custos_placa += `</div>`;
    return let_conteudo_div_tab_resumo_custos_placa;
}

function gera_estrutura_custos_placa_contas(dic_resumo_contas){

    let let_conteudo_div_tab_resumo_placa_contas = ``;

    dic_resumo_contas.forEach(conta => {
        let_conteudo_div_tab_resumo_placa_contas += `

            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                <div class="d-flex flex-column justify-content-center align-items-start p-2" style="width: 40%;">
                    <span style="font-size: 12px; font-weight: 600;">
                        <button type='button'
                                name="btn_detalhes_lanc_placa_conta"
                                id="btn_detalhes_lanc_placa_conta_${conta.HANDLE_CONTA}"
                                class="btn btn-rounded btn-space"
                                value=${conta.handle_filial}_${conta.HANDLE_CONTA}_${conta.HANDLE_PROJETO}_${conta.PLACA}>
                            <i class="fa-solid fa-eye icon-color-e"></i>
                            ${conta.NOME_CONTA}
                        </button>
                    </span>
                </div>

                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">0,00</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${conta.VAL_LANC}</span>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-end p-2" style="width: 15%;">
                    <span style="font-size: 12px;font-weight: 600;">${conta.perc_realizado}%</span>
                </div>
            </div>
        `;
    });
    return let_conteudo_div_tab_resumo_placa_contas;
}

/* Fim funções Aba Resumo Placa */

function gera_estrutura_razao_filial_conta_proj_placa(dic_razao){
    let let_conteudo_razao = ``;
    dic_razao.forEach(razao => {
        let let_os = `
            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="background: #363636;">
                <div class="d-flex justify-content-between align-items-between p-2"
                     style="width: 20%; background-color: #363636 !important;color:#ffffff;font-weight: 400;">
                    OS
                </div>
                <div class="d-flex justify-content-between align-items-between p-2 ms-1"
                     style="width: 20%;background-color: #363636 !important;color:#ffffff;font-weight: 400;">
                    Item
                </div>
                <div class="d-flex justify-content-between align-items-between p-2 ms-1"
                     style="width: 20%;background-color: #363636 !important;color:#ffffff;font-weight: 400;">
                    Tipo
                </div>
                <div class="d-flex justify-content-between align-items-between p-2 ms-1"
                     style="width: 20%;background-color: #363636 !important;color:#ffffff;font-weight: 400;">
                    Conjunto
                </div>
            </div>
        `;
        razao.dic_os_razao.forEach( os => {
            let_os += `
                <div class="d-flex justify-content-between align-items-between w-100 p-2">
                    <div class="d-flex justify-content-start align-items-center p-1"
                         style="width: 20%;font-weight: 600;">
                         <i class="fa-solid fa-angle-right icon-color-e"></i>
                        ${os.codigo_os}
                    </div>
                    <div class="d-flex justify-content-start align-items-center p-1 ms-1"
                         style="width: 20%;font-weight: 400;">
                        ${os.desc_os}
                    </div>
                    <div class="d-flex justify-content-start align-items-center p-1 ms-1"
                         style="width: 20%;font-weight: 400;">
                        ${os.desc_produto}
                    </div>
                    <div class="d-flex justify-content-start align-items-center p-1 ms-1"
                         style="width: 20%;font-weight: 400;">
                        ${os.desc_conjunto}
                    </div>
                </div>
                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2 ms-1"
                     style="font-weight: 400;">
                    <b>Descrição OS :</b> ${os.desc_tipo_os}
                </div>
                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2 ms-1"
                     style="border-bottom: 1px dashed #BDB1A8;font-weight: 400;">
                    <b>Observação OS :</b> ${os.obs_os}
                </div>
            `;
        });

        let_conteudo_razao += `
            <div class="accordion-item mb-1">
                <h6 class="accordion-header" id="heading_razao_${razao.handle_lanc_cc}">
                    <button id="bnt_razao_os_${razao.num_doc_contabil}" name="bnt_razao_os"
                            value="${razao.num_doc_contabil}"
                            class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapse_razao_${razao.num_doc_contabil}" aria-expanded="false"
                            aria-controls="collapse_razao_${razao.num_doc_contabil}" style="font-size:12px;">


                        <div class="d-flex flex-column justify-content-between align-items-between w-100 p-2">
                            <div class="d-flex justify-content-between align-items-between w-100 p-2">
                                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-bookmark icon-color-e"></i>&nbsp;&nbsp;
                                        Núm. documento
                                    </span>
                                    <span class="d-flex justify-content-end align-items-end w-100 p-1" style="font-size: 12px; font-weight: 600;">
                                        ${razao.num_doc}
                                    </span>
                                </div>
                                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Lançamento
                                    </span>
                                    <span class="d-flex justify-content-end align-items-end w-100 p-1" style="font-size: 12px; font-weight: 600;">
                                        ${razao.data_lancamento}
                                    </span>
                                </div>
                                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Núm. doc. contábil
                                    </span>
                                    <span class="d-flex justify-content-end align-items-end w-100 p-1" style="font-size: 12px; font-weight: 600;">
                                        ${razao.num_doc_contabil}
                                    </span>
                                </div>
                            </div>

                            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Tipo conta
                                    </span>
                                    <span class="d-flex justify-content-end align-items-end w-100 p-1" style="font-size: 12px; font-weight: 600;">
                                        ${razao.desc_tipo_conta}
                                    </span>
                                </div>
                                <div class="d-flex flex-column justify-content-center align-items-start w-100 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Fornecedor
                                    </span>
                                    <span class="d-flex justify-content-end align-items-end w-100 p-1" style="font-size: 12px; font-weight: 600;">
                                        ${razao.nome_fornec}
                                    </span>
                                </div>
                            </div>

                            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                                <div class="d-flex flex-column justify-content-center align-items-start w-75 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Cluster
                                    </span>
                                    <span class="d-flex justify-content-end align-items-center w-100 p-1 ms-2" style="font-size: 12px; font-weight: 600;">
                                        ${razao.desc_cluster}
                                    </span>
                                </div>

                                <div class="d-flex flex-column justify-content-center align-items-start w-75 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Valor
                                    </span>
                                    <span class="d-flex justify-content-end align-items-center w-100 p-1 ms-2" style="font-size: 18px; font-weight: 800;">
                                        R$ ${razao.val_lanc}
                                    </span>
                                </div>
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                                <div class="d-flex flex-column justify-content-center align-items-start w-75 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Histórico
                                    </span>
                                    <span class="d-flex justify-content-start align-items-center w-100 p-1 ms-2" style="font-size: 12px; font-weight: 600;">
                                        ${razao.obs}
                                    </span>
                                </div>
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-100 p-2" style="border-top: 1px dashed #BDB1A8;">
                                <div class="d-flex justify-content-start align-items-center w-75 p-2">
                                    <span style="font-size: 12px; font-weight: 600;">
                                        <i class="fa-solid fa-caret-right icon-color-e"></i>&nbsp;&nbsp;
                                        Projeto: &nbsp;&nbsp;
                                    </span>
                                    <span style="font-size: 12px; font-weight: 600;">
                                        ${razao.nome_projeto}
                                    </span>
                                </div>
                            </div>

                        </div>


                    </button>
                </h6>
                <div id="collapse_razao_${razao.num_doc_contabil}" class="accordion-collapse collapse"
                     aria-labelledby="heading_razao_${razao.num_doc_contabil}" data-bs-parent="#accordion_razao_custos_frota">

                    <div class="accordion-body d-flex flex-column"
                         id="div_dados_os_filial_contas_proj_placa_${razao.num_doc_contabil}">

                         <div class="d-flex flex-column justify-content-between align-items-between w-100 p-2">
                            ${let_os}
                         </div>
                    </div>
                </div>
            </div>
        `;


    });

    return let_conteudo_razao;
}