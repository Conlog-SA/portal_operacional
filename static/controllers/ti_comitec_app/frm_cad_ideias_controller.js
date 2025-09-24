let let_dic_usu_sessao = null;
let let_count_tr_tarefas = 9999;
let let_count_tr_acoes = 9999;
let let_lista_usuarios = [];

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



$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_abre_modal_add_item_gut_g" || let_nome_btn == "btn_abre_modal_add_item_gut_u" ||
        let_nome_btn == "btn_abre_modal_add_item_gut_t") {
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/abre_modal_itens_gut',
            data: {
                'tipo_item_gut'  :   let_val_btn,
            },
            success: function (dados) {
                let let_head = `
                    ${dados.icon_head_modal_add_item_gut}
                      <span style="color:#ffffff; font-size:15px">
                          <strong>(${dados.desc_head_modal_add_item_gut})</strong>
                      </span>
                `;
                $("#p_head_modal_add_item_gut").html(let_head);

                let let_lista_itens_gut = [];
                dados.lista_itens_gut.forEach( item => {
                    let let_status = 'Sim';
                    if(item.ativo == 'N'){
                        let_status = 'Não';
                    }
                    let let_flag = `
                        <i class="${item.flag}" style="color:${item.color_flag}"></i>
                    `;
                    let reg = [
                        let_flag,
                        item.desc,
                        item.peso,
                        let_status
                    ];
                    let_lista_itens_gut.push(reg);
                });
                $('#tab_itens_gut').DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": true,
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 6,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_itens_gut,
                    "columns": [
                        { title: "" },
                        { title: "Item" },
                        { title: "Peso" },
                        { title: "Ativo?" }
                    ],
                    /*"columnDefs": [
                        {"className": "dt-center", "targets": [0,1,3,12,21,22,23,24,25,26,27]},
                        {"className": "dt-left", "targets": [2]},
                        {"className": "dt-right", "targets": [4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20]}
                    ],*/
                    "oLanguage": {
                        "sProcessing":   "Processando...",
                        "sLengthMenu":   "Mostrar _MENU_ registros",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
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
                $("#btn_add_item_gut").val(let_val_btn);
                $("#modal_add_item_gut").show();
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
    else if (let_nome_btn == "btn_fecha_modal_add_item_gut") {
        $("#modal_add_item_gut").hide();
    } else if (let_nome_btn == "btn_add_item_gut") {
        let let_desc_item = $("#txt_desc_item_gut").val();
        let let_peso_item = $("#txt_peso_item_gut").val();
        let let_tipo_item = $(this).val();
        if(let_desc_item != '' && let_peso_item != ''){
            $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/add_item_gut',
            data: {
                'desc_item'  :   let_desc_item,
                'peso_item' :   let_peso_item,
                'tipo_item' :   let_tipo_item
            },
            success: function (dados) {
                let let_lista_itens_gut = [];
                dados.lista_itens_gut.forEach( item => {
                    let let_status = 'Sim';
                    if(item.ativo == 'N'){
                        let_status = 'Não';
                    }
                    let reg = [
                        item.flag,
                        item.desc,
                        item.peso,
                        let_status
                    ];
                    let_lista_itens_gut.push(reg);
                });
                $('#tab_itens_gut').DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": true,
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 6,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_itens_gut,
                    "columns": [
                        { title: "" },
                        { title: "Item" },
                        { title: "Peso" },
                        { title: "Ativo?" }
                    ],
                    /*"columnDefs": [
                        {"className": "dt-center", "targets": [0,1,3,12,21,22,23,24,25,26,27]},
                        {"className": "dt-left", "targets": [2]},
                        {"className": "dt-right", "targets": [4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20]}
                    ],*/
                    "oLanguage": {
                        "sProcessing":   "Processando...",
                        "sLengthMenu":   "Mostrar _MENU_ registros",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
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
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#txt_desc_item_gut").val('');
                $("#txt_peso_item_gut").val('');
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
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Informe a descrição e peso para o item!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }


    }
    else if (let_nome_btn == "btn_add_nova_ideia_comitec") {
        let let_desc_ideia = $("#hd_desc_ideia_comitec").val();
        let let_resumo_ideia = $("#txt_resumo_ideia_comitec").val();
        if(let_desc_ideia == null || let_desc_ideia == '') {
            let_desc_ideia = let_resumo_ideia;
        }
        let let_cod_atividade = $("#cb_cod_area_resp_ideia_comitec").val();
        let let_cod_usu_owner = $("#cb_usu_owner_ideia_comitec").val();
        let let_num_chamado = $("#num_chamado_ideia_comitec").val();
        let let_data_ideia = $("#dt_ideia_comitec").val();
        let let_estimativa_val_ganhos = $("#val_ganhos_ideia_comitec").val();
        let let_estimativa_desp = $("#val_despesas_ideia_comitec").val();
        let let_estimativa_ganhos_horas = $("#txt_horas_ganho_ideia_comitec").val();
        let let_cod_usu_master = $("#cb_usu_master_ideia_comitec").val();
        let let_obs_usu_owner = $("#txt_obs_usu_owner").val();

        let let_lista_componente_campos_obgo = document.getElementsByClassName('cl_valida_campo_obgo');
        let let_elem_array = Array.from(let_lista_componente_campos_obgo);
        let let_campos_validados = 0;
        let_elem_array.forEach(campo => {
            if(campo.getAttribute('name') != null && (campo.value == '' || campo.value == null)){
                let_campos_validados += 1;
            }

        });
        if(let_campos_validados > 0) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Preencha todos os campos obrigatórios indicado pelo (*)!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            /* window.scroll({
                top: 0,
                behavior: 'smooth'
            }); */
            let let_loader_frm_cad_ideias_comitec = document.getElementById("loader_frm_cad_ideias_comitec");
            let_loader_frm_cad_ideias_comitec.style.display = "flex";
            $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/add_nova_ideia_comitec',
            data: {
                'cod_ideia': let_val_btn,
                'desc_ideia'  :   let_desc_ideia,
                'resumo_ideia': let_resumo_ideia,
                'cod_atividade' :   let_cod_atividade,
                'cod_usu_owner' :   let_cod_usu_owner,
                'obs_usu_owner': let_obs_usu_owner,
                'num_chamado' : let_num_chamado,
                'data_ideia': let_data_ideia,
                'estimativa_val_ganhos': let_estimativa_val_ganhos,
                'estimativa_desp': let_estimativa_desp,
                'estimativa_ganhos_horas': let_estimativa_ganhos_horas,
                'cod_usu_master': let_cod_usu_master,
                'obs_usu_owner': let_obs_usu_owner
            },
            success: function (dados) {

                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                if(dados.dic_usuario_sessao.tipo_colab_comitec == 'L'){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);

                }
                else if(dados.dic_usuario_sessao.tipo_colab_comitec == 'M'){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);


                }
                else if(dados.dic_usuario_sessao.tipo_colab_comitec == 'H' || dados.obj_usu_dic.tipo_colab_comitec == 'G'){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', false);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', false);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', false);

                    $("#txt_nota_usu_head_ideia_comitec").prop('disabled', false);
                    $("#txt_obs_usu_head").prop('disabled', false);
                    $("#btn_add_aval_usu_head_ideia_comitec").prop('disabled', false);
                }


                let let_img_btn_atualizar_ideia = `
                    <i class="fa-solid fa-rotate-right" style="color: #FFFFFF;"></i>
                    Atualizar idéia
                `;
                $("#btn_add_nova_ideia_comitec").val(dados.cod_ideia);
                $("#btn_add_nova_ideia_comitec").html(let_img_btn_atualizar_ideia);

                let btn_limpar_campos = `
                    <button type="button" name="btn_limpa_campos_frm_ideia_comitec"
                              id="btn_limpa_campos_frm_ideia_comitec"
                              class="btn btn-primary btn-rounded botaoPrincipal">
                        <i class="fa-regular fa-lightbulb" style="color: #FFFFFF;"></i>
                          Registrar Nova Idéia
                      </button>
                `;
                $("#div_btn_nova_ideia").html(btn_limpar_campos);

                carrega_tabela_ideias(dados.lista_ideias_frm);
                //limpa_campos_frm_ideia_comitec(dados.dic_usuario_sessao);

                $("#btn_add_aval_usu_master_ideia_comitec").val(dados.cod_ideia);
                $("#btn_add_aval_usu_head_ideia_comitec").val(dados.cod_ideia);
                $("#btn_confirma_peso_item_gut").val(dados.cod_ideia);


                let_loader_frm_cad_ideias_comitec.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_frm_cad_ideias_comitec.style.display = "none";
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
    else if (let_nome_btn == 'btn_detalhes_ideia_comitec'){
        $("#div_tab_ideias_comitec").removeClass('active');
        $("#a_tab_ideias_comitec").removeClass('active');
        $("#div_tab_cad_ideia_comitec").addClass('active');
        $("#a_tab_cad_ideia_comitec").addClass('active');
        let let_cod_ideia_comitec = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/retorna_ideia_comitec_by_id',
            data: {
                'cod_ideia_comitec'  :   let_cod_ideia_comitec
            },
            success: function (dados) {
                let_dic_usu_sessao = dados.obj_usu_dic;
                let let_flag_gut_g = `
                    <i class="${dados.ideia_dic.flag_gut_g}" style="color:${dados.ideia_dic.color_gut_g}"></i>
                `;
                $("#btn_abre_modal_add_nota_gut_g").html(let_flag_gut_g);
                $("#btn_abre_modal_add_nota_gut_g").attr('title', dados.ideia_dic.peso_gut_g);
                let let_flag_gut_u = `
                    <i class="${dados.ideia_dic.flag_gut_u}" style="color:${dados.ideia_dic.color_gut_u}"></i>
                `;
                $("#btn_abre_modal_add_nota_gut_u").html(let_flag_gut_u);
                $("#btn_abre_modal_add_nota_gut_u").attr('title', dados.ideia_dic.peso_gut_u);
                let let_flag_gut_t = `
                    <i class="${dados.ideia_dic.flag_gut_t}" style="color:${dados.ideia_dic.color_gut_t}"></i>
                `;
                $("#btn_abre_modal_add_nota_gut_t").html(let_flag_gut_t);
                $("#btn_abre_modal_add_nota_gut_t").attr('title', dados.ideia_dic.peso_gut_t);

                $("#txt_nota_tt_gut").val(dados.ideia_dic.nota_gut_tt);


                $("#num_chamado_ideia_comitec").val(dados.ideia_dic.cod_chamado);
                $("#div_desc_ideia_comitec").html(dados.ideia_dic.desc_ideia);
                $("#txt_resumo_ideia_comitec").val(dados.ideia_dic.resumo_ideia);
                $("#cb_cod_area_resp_ideia_comitec").val(dados.ideia_dic.cod_atividade);
                $("#cb_cod_area_resp_ideia_comitec").selectpicker("refresh");

                $("#cb_usu_owner_ideia_comitec").val(dados.ideia_dic.cod_usu_owner);
                $("#cb_usu_owner_ideia_comitec").selectpicker("refresh");

                $("#dt_ideia_comitec").val(dados.ideia_dic.data_lancamento_idea);
                $("#val_ganhos_ideia_comitec").val(dados.ideia_dic.val_ganhos);
                $("#val_despesas_ideia_comitec").val(dados.ideia_dic.val_despesas);
                $("#txt_horas_ganho_ideia_comitec").val(dados.ideia_dic.horas_ganhas);
                $("#txt_obs_usu_owner").val(dados.ideia_dic.obs_usu_owner);


                $("#btn_confirma_peso_item_gut").val(dados.ideia_dic.cod_ideia);

                let let_cod_usu_master = dados.ideia_dic.cod_usu_master;
                if ((let_cod_usu_master == '0') && (dados.obj_usu_dic.tipo_colab_comitec == 'M')){
                    $("#cb_usu_master_ideia_comitec").val(dados.obj_usu_dic.cod_usu_sessao);
                } else {
                    $("#cb_usu_master_ideia_comitec").val(let_cod_usu_master);
                }

                $("#cb_usu_master_ideia_comitec").selectpicker("refresh");
                $("#txt_obs_usu_master").val(dados.ideia_dic.obs_usu_master);

                let let_cod_usu_head = dados.ideia_dic.cod_usu_head;
                if ((let_cod_usu_head == '0') && (dados.obj_usu_dic.tipo_colab_comitec == 'H')){
                    $("#cb_usu_head_ideia_comitec").val(dados.obj_usu_dic.cod_usu_sessao);
                } else {
                    $("#cb_usu_head_ideia_comitec").val(let_cod_usu_head);
                }
                $("#cb_usu_head_ideia_comitec").selectpicker("refresh");
                $("#txt_nota_usu_head_ideia_comitec").val(dados.ideia_dic.nota_head);
                $("#txt_obs_usu_head").val(dados.ideia_dic.obs_usu_head);

                let let_lista_campos_usu_owner = document.getElementsByClassName('cl_valida_campo_obgo');
                let let_elem_owner_array = Array.from(let_lista_campos_usu_owner);

                let let_lista_campos_usu_master = document.getElementsByClassName('cl_campo_master');
                let let_elem_master_array = Array.from(let_lista_campos_usu_master);

                let let_lista_campos_usu_head = document.getElementsByClassName('cl_campo_head');
                let let_elem_head_array = Array.from(let_lista_campos_usu_head);

                if(dados.obj_usu_dic.tipo_colab_comitec == 'L'){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);
                    let_elem_owner_array.forEach(campo => {
                        campo.disabled = false;
                    });

                    let_elem_master_array.forEach(campo => {
                        campo.disabled = true;
                    });

                    let_elem_head_array.forEach(campo => {
                        campo.disabled = true;
                    });
                }
                else if(dados.obj_usu_dic.tipo_colab_comitec == 'M' ){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);
                    if( dados.obj_usu_dic.cod_usu_master == dados.obj_usu_dic.cod_usu_owner ){
                        let_elem_owner_array.forEach(campo => {
                            campo.disabled = false;
                        });
                    } else {
                        let_elem_owner_array.forEach(campo => {
                            campo.disabled = true;
                        });
                    }

                    let_elem_master_array.forEach(campo => {
                        campo.disabled = false
                    });

                    let_elem_head_array.forEach(campo => {
                        campo.disabled = true;
                    });

                     let let_img_btn_atualizar_ideia = `
                        <i class="fa-solid fa-rotate-right" style="color: #FFFFFF;"></i>
                        Atualizar idéia
                    `;
                    $("#btn_add_nova_ideia_comitec").val(dados.ideia_dic.cod_ideia);
                    $("#btn_add_nova_ideia_comitec").html(let_img_btn_atualizar_ideia);

                    let btn_limpar_campos = `
                        <button type="button" name="btn_limpa_campos_frm_ideia_comitec"
                                  id="btn_limpa_campos_frm_ideia_comitec"
                                  class="btn btn-primary btn-rounded botaoPrincipal">
                            <i class="fa-regular fa-lightbulb" style="color: #FFFFFF;"></i>
                              Registrar Nova Idéia
                          </button>
                    `;
                    $("#div_btn_nova_ideia").html(btn_limpar_campos);

                    $("#btn_add_aval_usu_master_ideia_comitec").val(dados.ideia_dic.cod_ideia);
                    $("#btn_add_aval_usu_head_ideia_comitec").val(dados.ideia_dic.cod_ideia);

                }
                else if(dados.obj_usu_dic.tipo_colab_comitec == 'H' || dados.obj_usu_dic.tipo_colab_comitec == 'G'){
                    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', false);
                    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', false);
                    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', false);

                    if( dados.obj_usu_dic.cod_usu_head == dados.obj_usu_dic.cod_usu_owner ){
                        let_elem_owner_array.forEach(campo => {
                            campo.disabled = false;
                        });
                    } else {
                         let_elem_owner_array.forEach(campo => {
                            campo.disabled = true;
                        });

                    }

                    $("#cb_usu_master_ideia_comitec").prop('disabled', false);
                    $("#txt_obs_usu_master").prop('disabled', true);

                    let_elem_head_array.forEach(campo => {
                        campo.disabled = false;
                    });

                }
                $(".selectpicker").selectpicker("refresh");

                let let_img_btn_atualizar_ideia = `
                    <i class="fa-solid fa-rotate-right" style="color: #FFFFFF;"></i>
                    Atualizar idéia
                `;
                $("#btn_add_nova_ideia_comitec").val(dados.ideia_dic.cod_ideia);
                $("#btn_add_nova_ideia_comitec").html(let_img_btn_atualizar_ideia);

                let btn_limpar_campos = `
                    <button type="button" name="btn_limpa_campos_frm_ideia_comitec"
                              id="btn_limpa_campos_frm_ideia_comitec"
                              class="btn btn-primary btn-rounded botaoPrincipal">
                        <i class="fa-regular fa-lightbulb" style="color: #FFFFFF;"></i>
                          Registrar Nova Idéia
                      </button>
                `;
                $("#div_btn_nova_ideia").html(btn_limpar_campos);

                $("#btn_add_aval_usu_master_ideia_comitec").val(dados.ideia_dic.cod_ideia);
                $("#btn_add_aval_usu_head_ideia_comitec").val(dados.ideia_dic.cod_ideia);



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
    else if(let_nome_btn == 'btn_abre_modal_add_nota_gut_g' || let_nome_btn == "btn_abre_modal_add_nota_gut_u" ||
        let_nome_btn == "btn_abre_modal_add_nota_gut_t") {

        $("#btn_fecha_modal_pontua_item_gut").prop('disabled', false);
        $("#btn_confirma_peso_item_gut").prop('disabled', false);
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/abre_modal_peso_item_gut_ideia',
            data: {
                'tipo_item_gut'  :   let_val_btn,
            },
            success: function (dados) {
                let let_head = `
                    ${dados.icon_head_modal_add_item_gut}
                      <span style="color:#ffffff; font-size:15px">
                          <strong>(${dados.desc_head_modal_add_item_gut})</strong>
                      </span>
                `;
                $("#p_head_modal_pontua_item_gut").html(let_head);
                $("#hd_tipo_item_gup_nota").val(let_val_btn);

                $("#cb_cod_item_gut option").remove();
                dados.lista_itens_gut.forEach(item => {
                    $("#cb_cod_item_gut").append(`<option value='${item.cod_item_gut}'>${item.desc}(${item.peso})</option>`);

                });
                $("#cb_cod_item_gut").selectpicker("");
                $("#cb_cod_item_gut").selectpicker('refresh');

                $("#modal_pontua_item_gut").show();
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
    else if(let_nome_btn == 'btn_fecha_modal_pontua_item_gut'){
        $("#modal_pontua_item_gut").hide();
    }
    else if (let_nome_btn == 'btn_confirma_peso_item_gut'){
        $("#btn_confirma_peso_item_gut").prop('disabled', true);
        $("#btn_fecha_modal_pontua_item_gut").prop('disabled', true);
        let let_cod_tipo_item_gut = $("#cb_cod_item_gut").val();
        let let_desc_tipo_item_gut = $("#hd_tipo_item_gup_nota").val();
        let let_cod_ideia = let_val_btn;
        let let_loader_frm_cad_ideias_comitec = document.getElementById("loader_princ_frm_cad_ideias_comitec");
        let_loader_frm_cad_ideias_comitec.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/pontua_ideia_nota_gut',
            data: {
                'cod_ideia': let_cod_ideia,
                'cod_tipo_item_gut'  :   let_cod_tipo_item_gut,
                'desc_tipo_item_gut': let_desc_tipo_item_gut
            },
            success: function (dados) {
                let let_flag_btn = `
                    <i class="${dados.flag_item_gut}" style="color:${dados.color_flag_gut}" title="${dados.peso_item_gut}"></i>
                `;
                $("#btn_abre_modal_add_nota_gut_"+let_desc_tipo_item_gut.toLowerCase()).html(let_flag_btn);
                $("#txt_nota_tt_gut").val(dados.nota_total_gut);
                $("#modal_pontua_item_gut").hide();
                carrega_tabela_ideias(dados.lista_ideias_frm);
                let_loader_frm_cad_ideias_comitec.style.display = "none";
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
    else if ( let_nome_btn == 'btn_limpa_campos_frm_ideia_comitec') {
        $("#btn_add_nova_ideia_comitec").val('0');
        let let_caption_btn = `
            <i class="fa-solid fa-check" style="color: #FFFFFF;"></i>Registrar Idéia
        `;
        $("#btn_add_nova_ideia_comitec").html(let_caption_btn);
        $("#div_btn_nova_ideia").html('');
        limpa_campos_frm_ideia_comitec(let_dic_usu_sessao);
    }
    else if(let_nome_btn == 'btn_add_aval_usu_master_ideia_comitec'){
        let let_cod_usu_master = $("#cb_usu_master_ideia_comitec").val();
        let let_obs_usu_master = $("#txt_obs_usu_master").val();
        let let_loader_frm_parecer_master_ideias_comitec = document.getElementById("loader_frm_parecer_master_ideias_comitec");
        let_loader_frm_parecer_master_ideias_comitec.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/atualiza_parecer_tecnico_ideia',
            data: {
                'cod_ideia'  :   let_val_btn,
                'cod_usu_master': let_cod_usu_master,
                'obs_usu_master': let_obs_usu_master
            },
            success: function (dados) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_parecer_master_ideias_comitec.style.display = "none";
            },
            error: function (request, status, error) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_parecer_master_ideias_comitec.style.display = "none";
          }
        });
    }
    else if(let_nome_btn == 'btn_add_aval_usu_head_ideia_comitec'){
        let let_cod_usu_head = $("#cb_usu_head_ideia_comitec").val();
        let let_nota_head = $("#txt_nota_usu_head_ideia_comitec").val();
        let let_obs_usu_head = $("#txt_obs_usu_head").val();
        if( let_nota_head == '' || let_nota_head == null){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Sr. Head. Informe a sua nota para registrar seu parecer!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            let let_loader_frm_parecer_head_ideias_comitec = document.getElementById("loader_frm_parecer_head_ideias_comitec");
            let_loader_frm_parecer_head_ideias_comitec.style.display = "flex";
            $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/atualiza_parecer_head_ideia',
            data: {
                'cod_ideia'  :   let_val_btn,
                'cod_usu_head': let_cod_usu_head,
                'nota_head': let_nota_head,
                'obs_usu_head': let_obs_usu_head
            },
            success: function (dados) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                carrega_tabela_ideias(dados.lista_ideias_frm);
                let_loader_frm_parecer_head_ideias_comitec.style.display = "none";
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

    }
    else if (let_nome_btn == "btn_abre_modal_muda_idea_proj") {
        $("#btn_cria_projeto").val(let_val_btn);
        $("#modal_criar_projeto").show();
    } else if (let_nome_btn == "btn_não_cria_projeto") {
        $("#btn_não_cria_projeto").val(let_val_btn);
        $("#modal_criar_projeto").hide();
    }
    else if (let_nome_btn == "btn_cria_projeto") {
        let let_cod_ideia = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/abrir_modal_edita_projeto',
            data: {
                'tipo_processo': 'novo',
                'cod_ideia'  :   let_cod_ideia,

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
                /*$("#div_nome_projeto_frm_edt_proj").html(dados.dic_projeto.nome_projeto);
                $("#div_nome_sponsor_frm_edt_proj").html(dados.dic_projeto.nome_sponsor);
                $("#div_nome_gerente_frm_edt_proj").html(dados.dic_projeto.nome_gerente);
                $("#div_fase_proj_frm_edt_proj").html(dados.dic_projeto.fase);
                $("#div_objetivo_projeto_frm_edt_proj").html(dados.dic_projeto.objetivos_proj);
                $("#div_riscos_projeto_frm_edt_proj").html(dados.dic_projeto.riscos);
                $("#porcenagem_barra").html(dados.dic_projeto.perc_progresso_acoes);*/
                carrega_tabela_ideias(dados.lista_ideias_frm);

                let_lista_usuarios = [];
                dados.lista_usuarios.forEach( usu => {
                    let reg = [
                        usu.cod_usu,
                        usu.login_usu
                    ];
                    let_lista_usuarios.push(reg);

                });
                /*
                let let_porcentagem_barra = dados.dic_projeto.perc_progresso_acoes;
                $("#td_evolucao_proj_"+let_val_btn).html(let_porcentagem_barra);
                */

                /* $("#modal_projeto").show(); */

                $("#modal_criar_projeto").hide();

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


    }  else if (let_nome_btn == "btn_fecha_modal_criar_proj") {
        $("#modal_criar_projeto").hide();
    } else if (let_nome_btn == "btn_abre_proj") {
        $("#modal_editar_projeto").show();
    } else if (let_nome_btn == "btn_fecha_modal_proj_frm_proj") {
        $("#modal_editar_projeto").hide();
    } else if (let_nome_btn == "btn_fecha_proj") {
        $("#modal_projeto").hide();
    } else if (let_nome_btn == "btn_add_tr_tarefas") {
        $("#div_desc_tarefa").html('');
        $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
        let let_cod_tarefa_anterior = $("#hd_cod_btn_selecionado").val();
        let let_icone_acao_clicar_btn_anterior =`
                       <i class="fa-solid fa-eye-slash" style="color: #fd9a49!important;"></i>
                   `;
        $("#btn_visualiza_acoes_tarefa_"+let_cod_tarefa_anterior).html(let_icone_acao_clicar_btn_anterior);
        let_count_tr_tarefas += 1;
        let let_cor_empresa = $("#hd_cor_empresa_hx").val();
        fn_add_tr_tarefa(let_count_tr_tarefas, null, let_cor_empresa);

    }
    else if (let_nome_btn == "btn_add_tr_acao") {
        let_count_tr_acoes += 1;
        let let_cor_empresa = $("#hd_cor_empresa_hx").val();
        fn_add_nova_tr_table_acoes(let_count_tr_acoes, null,0, let_cor_empresa);

    }
    else if (let_nome_btn == "btn_abre_modal_edita_proj_frm_lista_proj") {
        let let_cod_btn = let_id_btn.split('_')[3];
        let let_div_evolucao_projeto = document.getElementById("div_evolucao_projeto");
        let let_cod_projeto = let_val_btn;
        $("#hd_cod_projeto").val(let_cod_projeto);
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/abrir_modal_edita_projeto',
            data: {
                'tipo_processo': 'edicao',
                'cod_projeto'  :   let_cod_projeto,
            },
            dataType: 'json',
            success: function (dados) {
                $("#hd_desc_ideia_comitec").val(let_count_tr_tarefas);
                $("#hd_cod_usu_master").val(dados.dic_projeto.cod_usu_master);
                $("#div_nome_projeto_frm_edt_proj").html(dados.dic_projeto.nome_projeto);
                $("#div_nome_sponsor_frm_edt_proj").html(dados.dic_projeto.nome_sponsor);
                $("#div_nome_gerente_frm_edt_proj").html(dados.dic_projeto.nome_gerente);
                $("#div_objetivo_projeto_frm_edt_proj").html(dados.dic_projeto.objetivos_proj);
                $("#div_riscos_projeto_frm_edt_proj").html(dados.dic_projeto.riscos);
                $("#sl_fase_proj_modal_edita_proj").val(dados.dic_projeto.desc_fase);
                $("#div_atualizacao_proj_frm_edt_proj").html(dados.dic_projeto.ult_atualização);
                $("#div_data_ini_proj_frm_edt_proj").html(dados.dic_projeto.data_inicio);
                $("#div_data_fim_proj_frm_edt_proj").html(dados.dic_projeto.data_fim);
                $("#porcenagem_barra").html(dados.dic_projeto.perc_progresso_acoes);
                $("#btn_finaliza_projeto").val(dados.dic_projeto.status_proj);
                if (dados.dic_projeto.cronograma == '0'){
                    $("#div_status_cronograma_proj").html(`<i class="fa-solid fa-circle fa-xl"
                        style="color:#3CB371!important;font-size: 1.5em!important;"></i>`);
                } else if (dados.dic_projeto.cronograma == '1'){
                    $("#div_status_cronograma_proj").html(`<i class="fa-solid fa-circle fa-xl"
                        style="color:#FFD700!important;font-size: 1.5em!important;"></i>`);
                } else if (dados.dic_projeto.cronograma == '2'){
                    $("#div_status_cronograma_proj").html(`<i class="fa-solid fa-circle fa-xl"
                        style="color:#FF0000!important;font-size: 1.5em!important;"></i>`);
                }

                let_div_evolucao_projeto.style.width = dados.dic_projeto.perc_progresso_acoes;

                let_lista_usuarios = [];
                $("#cb_usuarios_projeto option").remove();
                dados.lista_usuarios.forEach( usu => {
                    let reg = [
                        usu.cod_usu,
                        usu.login_usu
                    ];
                    let_lista_usuarios.push(reg);

                    let let_item_selected = ``;
                    dados.dic_projeto.lista_cod_usuarios_vinculados.forEach( cod_usu_vinc => {
                        if( cod_usu_vinc.cod_usu__cod_usu == usu.cod_usu){
                            let_item_selected = `selected="selected"`;
                        }
                    });

                    $("#cb_usuarios_projeto").append(`
                        <option value="${usu.cod_usu}" ${let_item_selected}>${usu.nome_usu}</option>
                    `);

                });
                if(dados.usu_logado_edt_proj == 'nok'){
                    $("#cb_usuarios_projeto").prop("disabled", true)
                    $("#sl_fase_proj_modal_edita_proj").prop("disabled", true);
                    $("#btn_add_tr_tarefas").prop("disabled", true);
                    $("#btn_add_tr_acao").prop("disabled", true);
                    $("#btn_finaliza_projeto").prop("disabled", true);

                }
                $("#cb_usuarios_projeto").selectpicker('refresh');

                let let_porcentagem_barra = dados.dic_projeto.perc_progresso_acoes;
                if ( let_porcentagem_barra != '100%' ){
                    $("#key").prop("disabled", false);
                    if(dados.usu_logado_edt_proj == 'ok'){
                        $("#btn_add_tr_tarefas").prop("disabled", false);
                    } else {
                        $("#btn_add_tr_tarefas").prop("disabled", true);
                    }
                    $("#btn_finaliza_projeto").prop("disabled", true);
                    let_btn_finalizado =`FINALIZAR PROJETO`;
                    $("#btn_finaliza_projeto").html(let_btn_finalizado);
                } else if ( let_porcentagem_barra == '100%' ) {
                    if(dados.usu_logado_edt_proj == 'ok'){
                        $("#btn_finaliza_projeto").prop("disabled", false);
                    } else {
                        $("#btn_finaliza_projeto").prop("disabled", true);
                    }
                    let let_btn_finaliza_projeto = dados.dic_projeto.status_proj;
                    if ( let_btn_finaliza_projeto == 1 ){
                        let_btn_finalizado =`PROJETO FINALIZADO`;
                        $("#btn_finaliza_projeto").html(let_btn_finalizado);
                        $("#btn_finaliza_projeto").prop("disabled", true);
                        $("#btn_add_tr_tarefas").prop("disabled", true);
                        $("#btn_add_tr_acao").prop("disabled", true);
                        $("#key").prop("disabled", true);
                        $("#btn_salvar_tarefa").prop("disabled", true);
                        $("#td_desc_tarefa_"+let_cod_btn).prop("contenteditable", false);
                    } else if ( let_btn_finaliza_projeto == 0 && dados.usu_logado_edt_proj == 'ok'){
                        let_btn_finalizado =`FINALIZAR PROJETO`;
                        $("#btn_finaliza_projeto").html(let_btn_finalizado);
                        $("#btn_finaliza_projeto").prop("disabled", false);
                        $("#key").prop("disabled", false);
                        $("#btn_add_tr_tarefas").prop("disabled", false);
                    }
                }

                $("#modal_projeto").show();
                //$("#btn_add_tr_acao").prop("disabled", true);
                $("#div_desc_tarefa").html('');
                fn_add_tr_tarefa(0, dados.lista_dic_tarefas, dados.cor_emp_hex);
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

    } else if (let_nome_btn == "btn_fecha_modal_edt_proj") {
        $("#tb_tarefas tr[name='tr_tarefa']").remove();
        $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
        $("#hd_cod_tarefa_selecionada").val('0');
        $("#modal_projeto").hide();
        let_count_tr_tarefas = 9999;
        let_count_tr_acoes = 9999;
    }
     else  if (let_nome_btn == "btn_fecha_modal_proj") {
        $("#modal_criar_projeto").hide();
    } else  if (let_nome_btn == "btn_salvar_tarefa") {
        $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
        let let_cod_projeto = $("#hd_cod_projeto").val();
        let let_cod_tarefa = $(this).val();
        let let_cod_btn = let_id_btn.split('_')[3];
        let let_cod_btn_anterior = $("#hd_cod_btn_selecionado").val();
        let let_desc_tarefa = $("#td_desc_tarefa_"+let_cod_btn).html();
        let let_cod_usu_master = $("#hd_cod_usu_master").val();
        let let_cor_empresa = $("#hd_cor_empresa_hx").val();

        $.ajax({
            type: 'POST',
            url: '/ti_comitec_app/salva_edita_tarefa',
            dataType: 'json',
            data: {
                'cod_projeto': let_cod_projeto,
                'cod_tarefa': let_cod_tarefa,
                'desc_tarefa': let_desc_tarefa,
            },
            success: function (dados) {
                let let_titulo_acao = `<strong>Tarefa: </strong>${dados.desc_tarefa}`;
                $("#div_desc_tarefa").html(let_titulo_acao);
                $("#hd_cod_tarefa_selecionada").val(dados.cod_tarefa);
                $("#hd_cod_btn_selecionado").val(let_cod_btn)
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let let_imagem_editar = `
                    <i class="fa-solid fa-pen-to-square" style="color: #fd9a49!important;"></i>
                `;
                $("#btn_salvar_tarefa_"+let_cod_btn).val(dados.cod_tarefa);
                $("#btn_salvar_tarefa_"+let_cod_btn).html(let_imagem_editar);

                let let_imagem_visualizar = `
                    <i class="fa-solid fa-eye" style="color: #3CB371!important;"></i>
                `;
                $("#btn_visualiza_acoes_tarefa_"+let_cod_btn).val(dados.cod_tarefa);
                $("#btn_visualiza_acoes_tarefa_"+let_cod_btn).prop('disabled', false);
                $("#btn_visualiza_acoes_tarefa_"+let_cod_btn).html(let_imagem_visualizar);


                if( let_cod_btn != let_cod_btn_anterior){
                    let img_btn_anterior = `
                        <i class="fa-solid fa-eye-slash" style="color: #fd9a49!important;"></i>
                    `;
                    $("#btn_visualiza_acoes_tarefa_"+let_cod_btn_anterior).html(img_btn_anterior);

                }

                let let_cod_tarefa_anterior = $("#hd_cod_tarefa_selecionada").val();
                if (let_cod_btn !== let_cod_tarefa_anterior) {
                    $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
                }
                fn_add_nova_tr_table_acoes(0, dados.lista_dic_acoes,let_cod_usu_master, let_cor_empresa);

                if(let_cod_tarefa == '0'){
                    let_count_tr_acoes += 1;
                    $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
                    fn_add_nova_tr_table_acoes(let_count_tr_acoes, null,let_cod_usu_master, let_cor_empresa);

                }
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
    else  if (let_nome_btn == "btn_salvar_acao") {
        let let_cod_btn = let_id_btn.split('_')[3];
        let let_desc_acao = $("#td_desc_acao_"+let_cod_btn).html();
        let let_prazo = $("#dt_prazo_frm_edt_acao_"+let_cod_btn).val();
        let let_cod_usu_atribuido = $("#sl_usu_frm_edt_acao_"+let_cod_btn).val();
        let let_cor_empresa = $("#hd_cor_empresa_hx").val();
        if((let_desc_acao != null && let_desc_acao != '') && (let_prazo != null && let_prazo!= '')) {
            let let_cod_projeto = $("#hd_cod_projeto").val();
            let let_cod_acao = $(this).val();

            let let_cod_atividade_pai = $("#hd_cod_tarefa_selecionada").val();

            let let_observacao = $("#td_observacao_"+let_cod_btn).html();
            $.ajax({
                type: 'POST',
                url: '/ti_comitec_app/salva_edita_acao',
                dataType: 'json',
                data: {
                    'cod_projeto': let_cod_projeto,
                    'cod_acao': let_cod_acao,
                    'cod_atividade_pai': let_cod_atividade_pai,
                    'desc_acao': let_desc_acao,
                    'observacao': let_observacao,
                    'prazo': let_prazo,
                    'cod_usu_atribuido': let_cod_usu_atribuido
                },
                success: function (dados) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    let let_imagem_editar = `
                        <i class="fa-solid fa-pen-to-square" style="color: #fd9a49!important;"></i>
                    `;
                    $("#btn_salvar_acao_"+let_cod_btn).val(dados.cod_acao);
                    $("#btn_salvar_acao_"+let_cod_btn).html(let_imagem_editar);


                    $("#btn_inicia_acao_"+let_cod_btn).prop('disabled', false);
                    $("#btn_inicia_acao_"+let_cod_btn).val(dados.cod_acao);

                    if(let_cod_acao == '0'){
                        let_count_tr_acoes += 1;
                        fn_add_nova_tr_table_acoes(let_count_tr_acoes, null,0, let_cor_empresa);
                    }

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
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Descrição e/ou prazo da ação, não informados!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }


    }
    else  if (let_nome_btn == "btn_visualiza_acoes_tarefa") {
        $("#tb_acoes_modal_edt_proj tr[name='tr_acao']").remove();
        $("#div_desc_tarefa").html('');
        $("#dt_prazo_frm_edt_acao").val('');
        $("#td_inicia_acao").val('');
        let let_cod_tarefa = let_val_btn;
        let let_cod_btn = let_id_btn.split('_')[4];
        let let_cor_emp_hex = $("#hd_cor_empresa_hx").val();

        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/retorna_acoes_tarefa',
            dataType: 'json',
            data: {
                'cod_tarefa': let_cod_tarefa
            },
            success: function (dados) {
                $("#div_desc_tarefa").html(`<strong style="color: #FFFFFF;">Tarefa: </strong>${dados.desc_tarefa}`);
                let let_icone_acao_clicar =`
                    <i class="fa-solid fa-eye" style="color: #3CB371!important;"></i>
                `;
                $("#btn_visualiza_acoes_tarefa_"+let_cod_btn).html(let_icone_acao_clicar);
                /* Altera icone do btn anterior q foi clicado*/
                let let_cod_tarefa_anterior = $("#hd_cod_btn_selecionado").val();
                if( let_cod_tarefa_anterior != '0'){
                    let let_icone_acao_clicar_btn_anterior =`
                        <i class="fa-solid fa-eye-slash" style="color: ${let_cor_emp_hex}"></i>
                    `;
                $("#btn_visualiza_acoes_tarefa_"+let_cod_tarefa_anterior).html(let_icone_acao_clicar_btn_anterior);
                }
                $("#hd_cod_tarefa_selecionada").val(let_cod_btn);
                $("#hd_cod_btn_selecionado").val(let_cod_btn);
                $("#dt_prazo_frm_edt_acao").val(dados.data_fim);
                if(dados.usu_logado_edt_proj == 'ok'){
                    $("#btn_add_tr_acao").prop("disabled", false);
                }

                fn_add_nova_tr_table_acoes(0, dados.lista_dic_acoes, 0, let_cor_emp_hex);
                let let_btn_finaliza_projeto = $("#btn_finaliza_projeto").val();
                if ( let_btn_finaliza_projeto == 1 ){
                    $("#btn_add_tr_acao").prop("disabled", true);
                }
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
    else  if (let_nome_btn == "btn_inicia_acao") {
        let let_cod_btn = let_id_btn.split('_')[3];
         let let_data_ini = $("#td_inicia_acao_"+let_cod_btn).html()
         let let_cod_acao = $(this).val();
         $.ajax({
            type: 'PUT',
            url: '/ti_comitec_app/inicia_acao',
            dataType: 'json',
            data: {
                'tipo_data': 'data_ini',
                'cod_acao': let_cod_acao,
                'cod_projeto': let_cod_acao
            },
            success: function (dados) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let let_data_ini = dados.data_ini.split('-')[2]+'-'+dados.data_ini.split('-')[1]+'-'+dados.data_ini.split('-')[0]
                $("#td_inicia_acao_"+let_cod_btn).html(let_data_ini);
                $("#btn_concluir_acao_"+let_cod_btn).prop("disabled", false);
                $("#btn_concluir_acao_"+let_cod_btn).val(dados.cod_acao);

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
    else  if (let_nome_btn == "btn_concluir_acao") {
        let let_cod_btn = let_id_btn.split('_')[3];
         let let_data_conclusao= $("#btn_concluir_acao_"+let_cod_btn).html()
         let let_cod_acao = $(this).val();
         $.ajax({
            type: 'PUT',
            url: '/ti_comitec_app/conclui_acao',
            dataType: 'json',
            data: {
                'tipo_data': 'data_conclusao',
                'cod_acao': let_cod_acao
            },
            success: function (dados) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let let_data_conclusao = dados.data_conclusao.split('-')[2]+'-'+dados.data_conclusao.split('-')[1]+'-'+dados.data_conclusao.split('-')[0]
                $("#td_conclui_acao_"+let_cod_btn).html(let_data_conclusao);
                $("#td_desc_acao_"+let_cod_btn).prop("contenteditable", false);
                $("#td_observacao_"+let_cod_btn).prop("contenteditable", false);
                $("#btn_salvar_acao_"+let_cod_btn).prop("disabled", true);
                $("#dt_prazo_frm_edt_acao_"+let_cod_btn).prop('disabled', true);
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
    else  if (let_nome_btn == "btn_finaliza_projeto") {
         let let_cod_projeto = $("#hd_cod_projeto").val();
         let let_cod_btn = let_id_btn.split('_')[3];

         $.ajax({
            type: 'PUT',
            url: '/ti_comitec_app/finaliza_projeto',
            dataType: 'json',
            data: {
                'cod_projeto': let_cod_projeto,
            },
            success: function (dados) {
                $("#btn_finaliza_projeto").val(dados.status_proj);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let let_btn_finaliza_projeto = dados.status_proj;
                if ( let_btn_finaliza_projeto == 1 ){
                    let_btn_finalizado =`PROJETO FINALIZADO`;
                    $("#btn_finaliza_projeto"+let_cod_btn).html(let_btn_finalizado);
                } else {
                    let_btn_finalizado =`FINALIZAR PROJETO`;
                    $("#btn_finaliza_projeto"+let_cod_btn).html(let_btn_finalizado);
                }

                $("#btn_finaliza_projeto").prop("disabled", true);
                $("#sl_fase_proj_modal_edita_proj").prop("disabled", true);
                $("#sl_fase_proj_modal_edita_proj").val(3);
                $("#td_desc_tarefa").prop("contenteditable", false);

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
    else if ( let_nome_btn == "btn_atualizar_dados_tab_acoes_proj_comitec") {
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/atualiza_tab_prox_acoes_proj',
            dataType: 'json',
            success: function (dados) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let let_lista_acoes = []
                dados.lista_obj_acoes_prox_ou_atradadas.forEach(acao => {
                    let let_img_status_acao = `
                        <i class="fa-solid fa-thumbs-up" style="color:#6495ED!important;" title="Em andamento"></i>
                    `;
                    if(acao.status == "Concluída"){
                        let_img_status_acao = `
                            <i class="fa-solid fa-thumbs-up" style="color:#3CB371!important;" title="Concluída"></i>
                        `;
                    } else if(acao.status == "Atrasada"){
                        let_img_status_acao = `
                            <i class="fa-solid fa-thumbs-down" style="color:#FF0000!important;" title="Atrasada"></i>
                        `;
                    }

                    let let_cronograma_projeto = `
                        <i class="fa-solid fa-circle fa-xl" style="color:#00FA9A!important;" title="Dentro do esperado"></i>
                    `;
                    if(acao.cronograma_projeto == 1){
                        let_cronograma_projeto = `
                            <i class="fa-solid fa-circle fa-xl" style="color:#FFD700!important;" title="Em risco"></i>
                        `;
                    } else if(acao.cronograma_projeto == 2){
                        let_cronograma_projeto = `
                            <i class="fa-solid fa-circle fa-xl" style="color:#FF0000!important;" title="Atrasado"></i>
                        `;
                    }

                    let let_btn_editar_projeto = `
                        <button class='btn btn-rounded btn-space'
                                id="btn_abre_modal_edita_proj_frm_lista_proj_{{acao.cod_projeto}}"
                                name="btn_abre_modal_edita_proj_frm_lista_proj"
                                value="${acao.cod_projeto}" title="Ver detalhes projeto">
                            <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                        </button>
                    `;


                    let reg = [
                        let_img_status_acao,
                        acao.login_master,
                        acao.desc_projeto,
                        let_cronograma_projeto,
                        acao.desc_acao,
                        acao.prazo,
                        acao.data_ultima_atualizacao_proj,
                        let_btn_editar_projeto
                    ]
                    let_lista_acoes.push(reg);
                });
                $('#tab_acoes_proj_comitec').DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": '50vh',
                    "scrollX": true,
                    "scrollCollapse": true,
                    //"paging": true,
                    //"pageLength": 6,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_acoes,
                    "columns": [
                        { title: "Status" },
                        { title: "Usuário" },
                        { title: "Projeto" },
                        { title: "Cronograma" },
                        { title: "Ação" },
                        { title: "Prazo" },
                        { title: "Últ. Atualização Proj." },
                        { title: "Abrir" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,1,3,5,6,7]},
                        {"className": "dt-left", "targets": [2,4]}
                    ],
                    "oLanguage": {
                        "sProcessing":   "Processando...",
                        "sLengthMenu":   "Mostrar _MENU_ registros",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
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


            },error: function (request, status, error) {
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


function carrega_tabela_ideias(lista_ideias_frm) {
    let let_lista_ideias = [];
    lista_ideias_frm.forEach( ideia => {
        let let_btn_detalhes = `
            <button type='button' name='btn_detalhes_ideia_comitec'
                id='btn_detalhes_ideia_comitec_${ideia.cod_ideia}'
                class='btn btn-rounded btn-space'
                value='${ideia.cod_ideia}' title='Clique para ver os detalhes da idéia'>
                <i class="fa-solid fa-eye" style="color: #f46424;"></i>
            </button>
        `;

        let let_btn_converter_ideia_em_proj = `
            <button type='button' name='btn_abre_modal_muda_idea_proj'
                    id='btn_abre_modal_muda_idea_proj_${ideia.cod_ideia}'
                    class="btn btn-sm btn-primary btn-rounded" value="${ideia.cod_ideia}"
                    style="border-radius: 5rem;border-color: #ffffff; background-color: transparent;"
                    title='Transformar idéia em projeto'>
                <i class="fa-solid fa-play fa-beat" style="color: #32930C; width: 40px;"></i>
            </button>
        `;

        let let_flag_gut_g = `
            <i class="${ideia.flag_gut_g}" style="color:${ideia.color_flag_gut_g}" title="${ideia.nota_gut_g}(${ideia.desc_gut_g})"></i>
        `;
        let let_flag_gut_u = `
            <i class="${ideia.flag_gut_u}" style="color:${ideia.color_flag_gut_u}" title="${ideia.nota_gut_u}(${ideia.desc_gut_u})"></i>
        `;
        let let_flag_gut_t = `
            <i class="${ideia.flag_gut_t}" style="color:${ideia.color_flag_gut_t}" title="${ideia.nota_gut_t}(${ideia.desc_gut_t})"></i>
        `;

        let reg = [
            let_flag_gut_g,
            let_flag_gut_u,
            let_flag_gut_t,
            ideia.nota_total,
            ideia.nota_gut,
            ideia.nota_head,
            ideia.nome_empresa,
            ideia.desc_area,
            ideia.resumo_ideia,
            ideia.login_owner,
            ideia.login_master,
            ideia.login_head,
            let_btn_detalhes,
            let_btn_converter_ideia_em_proj
        ];
        let_lista_ideias.push(reg);
    });
    let let_cab_g = `<i class="fa-solid fa-g" style="color: #f46424; width: 40px;"></i>`;
    let let_cab_u = `<i class="fa-solid fa-u" style="color: #f46424; width: 40px;"></i>`;
    let let_cab_t = `<i class="fa-solid fa-t" style="color: #f46424; width: 40px;"></i>`;
    $('#tab_ideias_comitec').DataTable( {
        "bJQueryUI": true,
        "destroy": true,
        "fixedHeader": true,
        "scrollY": true,
        "scrollX": true,
        "scrollCollapse": true,
        "paging": true,
        "pageLength": 6,
        "dom": 'Bfrtip',
        "buttons": [
            'copyHtml5'
        ],
        "data":let_lista_ideias,
        "columns": [
            { title: let_cab_g },
            { title: let_cab_u },
            { title: let_cab_t },
            { title: "Nota TT" },
            { title: "Nota GUT" },
            { title: "Nota Head" },
            { title: "Empresa" },
            { title: "Área" },
            { title: "Descrição Idéia" },
            { title: "Owner" },
            { title: "Master" },
            { title: "Head" },
            { title: "Detalhes" },
            { title: "Projeto" }
        ],
        "columnDefs": [
            {"className": "dt-center", "targets": [0,1,2,3,4,5,6,12,13]},
            {"className": "dt-left", "targets": [7,8]},
            {"className": "dt-right", "targets": [9,10,11]}
        ],
        "oLanguage": {
            "sProcessing":   "Processando...",
            "sLengthMenu":   "Mostrar _MENU_ registros",
            "sZeroRecords":  "Não foram encontrados resultados",
            "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
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


}


$(document).on('change','input', function(){
	let let_nome_inp = $(this).attr('name');
    let let_id_inp = $(this).attr('id');
    let let_val_inp = $(this).attr('value');

    if (let_nome_inp == "num_chamado_ideia_comitec") {
        let let_cod_chamado = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/ti_comitec_app/retorna_dados_chamados',
            data: {
                'cod_chamado'  :   let_cod_chamado,
            },
            success: function (dados) {
                $("#hd_desc_ideia_comitec").val(dados.dic_chamado.desc_problema);
                $("#div_desc_ideia_comitec").html(dados.dic_chamado.desc_problema);
                $("#dt_ideia_comitec").val(dados.dic_chamado.data_chamado);

                $("#cb_usu_owner_ideia_comitec").val(dados.dic_chamado.cod_usu_abertura);
                $("#cb_usu_owner_ideia_comitec").selectpicker('refresh');

                $("#cb_usu_master_ideia_comitec").val(dados.dic_chamado.cod_usu_atendente);
                $("#cb_usu_master_ideia_comitec").selectpicker('refresh');
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
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


function limpa_campos_frm_ideia_comitec(dic_usuario){
    let let_img_flags = `
        <i class="fa-regular fa-flag" style="color: #f46424; width: 40px;"></i>
    `;
    $("#btn_abre_modal_add_nota_gut_g").html(let_img_flags);
    $("#btn_abre_modal_add_nota_gut_u").html(let_img_flags);
    $("#btn_abre_modal_add_nota_gut_t").html(let_img_flags);
    $("#txt_nota_tt_gut").val("0");

    $("#num_chamado_ideia_comitec").val('');
    $("#div_desc_ideia_comitec").html('');
    $("#txt_resumo_ideia_comitec").val('');
    $("#cb_cod_area_resp_ideia_comitec").val('');
    $("#cb_cod_area_resp_ideia_comitec").selectpicker("refresh");



    $("#dt_ideia_comitec").val('');
    $("#val_ganhos_ideia_comitec").val('');
    $("#val_despesas_ideia_comitec").val('');
    $("#txt_horas_ganho_ideia_comitec").val('');
    $("#txt_obs_usu_owner").val('');

    let let_lista_campos_usu_owner = document.getElementsByClassName('cl_valida_campo_obgo');
    let let_elem_owner_array = Array.from(let_lista_campos_usu_owner);

    let let_lista_campos_usu_master = document.getElementsByClassName('cl_campo_master');
    let let_elem_master_array = Array.from(let_lista_campos_usu_master);

    let let_lista_campos_usu_head = document.getElementsByClassName('cl_campo_head');
    let let_elem_head_array = Array.from(let_lista_campos_usu_head);

    $("#txt_nota_usu_head_ideia_comitec").val('');

    $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
    $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
    $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);


    if(dic_usuario.tipo_colab_comitec == 'L'){
        /*$("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
        $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
        $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true);*/

        let_elem_owner_array.forEach(campo => {
            campo.disabled = false;
        });

        let_elem_master_array.forEach(campo => {
            campo.disabled = true;
        });

        let_elem_head_array.forEach(campo => {
            campo.disabled = true;
        });

        $("#cb_usu_owner_ideia_comitec").val(dic_usuario.cod_usu);
        $("#cb_usu_master_ideia_comitec").val('');
        $("#cb_usu_head_ideia_comitec").val('');
    }
    else if(dic_usuario.tipo_colab_comitec == 'M'){
        /* $("#btn_abre_modal_add_nota_gut_g").prop('disabled', true);
        $("#btn_abre_modal_add_nota_gut_u").prop('disabled', true);
        $("#btn_abre_modal_add_nota_gut_t").prop('disabled', true); */
        let_elem_owner_array.forEach(campo => {
            campo.disabled = false;
        });

        let_elem_master_array.forEach(campo => {
            campo.disabled = false;
        });

        let_elem_head_array.forEach(campo => {
            campo.disabled = true;
        });

        $("#cb_usu_owner_ideia_comitec").val(dic_usuario.cod_usu);
        $("#cb_usu_master_ideia_comitec").val(dic_usuario.cod_usu);
        $("#cb_usu_head_ideia_comitec").val('');
    }
    else if(dic_usuario.tipo_colab_comitec == 'H' || dic_usuario.tipo_colab_comitec == 'G'){
        /* $("#btn_abre_modal_add_nota_gut_g").prop('disabled', false);
        $("#btn_abre_modal_add_nota_gut_u").prop('disabled', false);
        $("#btn_abre_modal_add_nota_gut_t").prop('disabled', false); */
        let_elem_owner_array.forEach(campo => {
            campo.disabled = false;
        });

        let_elem_master_array.forEach(campo => {
            campo.disabled = false;
        });

        let_elem_head_array.forEach(campo => {
            campo.disabled = false;
        });
        $("#cb_usu_owner_ideia_comitec").val(dic_usuario.cod_usu);
        $("#cb_usu_master_ideia_comitec").val(dic_usuario.cod_usu);
        $("#cb_usu_head_ideia_comitec").val(dic_usuario.cod_usu);

    }
    $(".selectpicker").selectpicker("refresh");
    let_dic_usu_sessao = null;
    window.scroll({
        top: 0,
        behavior: 'smooth'
    });
};


$(document).on('change','#sl_fase_proj_modal_edita_proj', function(){
    let let_cod_projeto = $("#hd_cod_projeto").val();
    let let_fase_projeto = $(this).val();

    $.ajax({
        type: 'POST',
        url: '/ti_comitec_app/abrir_modal_edita_projeto',
        data: {
            'cod_projeto'  :   let_cod_projeto,
            'fase_projeto' :   let_fase_projeto
        },
        success: function (dados) {
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
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

});



function fn_add_tr_tarefa(cod_linha, lista_tarefas, cor_empresa_hex) {
    if(lista_tarefas == null) {

        $(`
            <tr style="background-color: #e9e9e9c4; font-size: 0.5rem!important;" name="tr_tarefa" class='scroll'>
                <td style="padding: 0.25rem;align-content: center;">
                    &nbsp;
                </td>
                <td contenteditable='true' name='td_desc_tarefa' id="td_desc_tarefa_${cod_linha}"
                    style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal;align-content: center;">
                </td>
                <td style="padding: 0.25rem;align-content: center;">
                    &nbsp;
                </td>
                <td style="padding: 0.25rem;align-content: center;">
                    &nbsp;
                </td>
                <td style="padding: 0.25rem;align-content: center;">
                    &nbsp;
                </td>
                <td align="center" style="align-content: center;">
                    <button name='btn_salvar_tarefa' id="btn_salvar_tarefa_${cod_linha}" value="0"
                        class="btn btn-rounded btn-space" style="width: 35px;" title="Salvar/Atualizar tarefa">
                            <i class="fa-solid fa-check" style="color: ${cor_empresa_hex}"></i>
                    </button>
                </td>
                <td style="align-content: center;">
                    &nbsp;
                </td>
                <td align="center" style="align-content: center;">
                    <button style="width: 35px;" value="0" class="btn btn-rounded btn-space" title="Visualizar ações"
                        name="btn_visualiza_acoes_tarefa" id="btn_visualiza_acoes_tarefa_${cod_linha}" disabled>
                        <i class="fa-solid fa-eye-slash" style="color: ${cor_empresa_hex}"></i>
                    </button>
                </td>
            </tr>
        `).insertAfter("#btnAddLineTarefa");
    }
    else {
        lista_tarefas.forEach( tarefa => {

            let let_btn_salva_tarefa = ``;
            let let_desc_tarefa = ``;
            let let_atrib = ``;
            let let_img_status_tarefa = `
                <i class="fa-solid fa-thumbs-up" style="color:#6495ED!important;" title="Em andamento"></i>
            `;
            let let_habilita_btn = ``;
            let let_edicao_td = `
                contenteditable='true'
            `;
            if(tarefa.status_edicao_campos == 'nok'){
                let_habilita_btn = `
                    disabled="disabled"
                `;
                let_edicao_td = `
                    contenteditable='false'
                `;
            }
            if(tarefa.status_tarefa == 'Concluída'){
                let_img_status_tarefa = `
                    <i class="fa-solid fa-thumbs-up" style="color:#3CB371!important;" title="Concluída"></i>
                `;
            } else if(tarefa.status_tarefa == 'Atrasada'){
                let_img_status_tarefa = `
                    <i class="fa-solid fa-thumbs-down" style="color:#FF0000!important;" title="Atrasada"></i>
                `;
            }

            if(tarefa.perc_progresso_tarefa != '100%') {
                let_btn_salva_tarefa = `
                    <button name='btn_salvar_tarefa' id="btn_salvar_tarefa_${tarefa.cod_atividade}"
                        class="btn btn-rounded btn-space" value="${tarefa.cod_atividade}" style="width: 35px;"
                        title="Salvar/Atualizar tarefa" ${let_habilita_btn}>
                            <i class="fa-solid fa-pen-to-square" style="color: ${cor_empresa_hex}"></i>
                    </button>
                `;
                let_desc_tarefa = `
                    <td ${let_edicao_td} name='td_desc_tarefa' id="td_desc_tarefa_${tarefa.cod_atividade}"
                        style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal;align-content: center;">
                            ${tarefa.desc_atividade}
                    </td>`;

            } else {
                let_btn_salva_tarefa = `
                    <button name='btn_salvar_tarefa' id="btn_salvar_tarefa_${tarefa.cod_atividade}"
                        class="btn btn-rounded btn-space" value="${tarefa.cod_atividade}" style="width: 35px;"
                        disabled="disabled" title="Salvar/Atualizar tarefa">
                            <i class="fa-solid fa-pen-to-square" style="color: ${cor_empresa_hex}"></i>
                    </button>`;
                let_desc_tarefa = `
                    <td contenteditable='false' name='td_desc_tarefa' id="td_desc_tarefa_${tarefa.cod_atividade}"
                        style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal;align-content: center;">
                            ${tarefa.desc_atividade}
                    </td>`;


            }


            $("#tb_tarefas").append(`
                <tr style="background-color: #e9e9e9c4; font-size: 0.5rem!important;" name="tr_tarefa" class='scroll'>
                    <td style="padding: 0.25rem;font-size: 10px;align-content: center;" align="center">
                        ${let_img_status_tarefa}
                    </td>
                   ${let_desc_tarefa}
                    <td style="padding: 0.25rem;font-size: 10px;align-content: center;" align="center">
                        ${tarefa.data_ini_tarefa}
                    </td>
                    <td style="padding: 0.25rem;font-size: 10px;align-content: center;" align="center">
                        ${tarefa.data_prazo_tarefa}
                    </td>
                    <td style="padding: 0.25rem;font-size: 10px;align-content: center;" align="center">
                        ${tarefa.data_termino_tarefa}
                    </td>
                    <td style="padding: 0.25rem;align-content: center;" align="center">
                        ${let_btn_salva_tarefa}
                    </td>
                    <td style="padding: 0.25rem;align-content: center;" align="right">
                        ${tarefa.perc_progresso_tarefa}
                    </td>
                    <td style="padding: 0.25rem;align-content: center;" align="center">
                        <button style="width: 35px;"  class="btn btn-rounded btn-space" value="${tarefa.cod_atividade}"
                            name="btn_visualiza_acoes_tarefa" id="btn_visualiza_acoes_tarefa_${tarefa.cod_atividade}"
                            title="Visualizar ações">
                                <i class="fa-solid fa-eye-slash" style="color: ${cor_empresa_hex}"></i>
                        </button>
                    </td>
                </tr>
            `);

        });
    }
}



function fn_add_nova_tr_table_acoes(cod_linha, lista_acoes, cod_usu_master, cor_empresa_hex) {
    if(lista_acoes == null) {
        let let_options_usu = '';
        for(let i=0; i <  let_lista_usuarios.length; i++){
            let let_selected = ``;
            if(let_lista_usuarios[i][0] == cod_usu_master){
                let_selected = `selected="selected"`;
            }
            let_options_usu += `
                <option value="${let_lista_usuarios[i][0]}" ${let_selected}>${let_lista_usuarios[i][1]}</option>
            `;
        }
       $(`
        <tr style="background-color: #e9e9e9c4;" name="tr_acao" class='scroll'>
            <td style="padding: 0.25rem;font-size: 10px;align-content: center;" align="center">
            </td>
            <td contenteditable='true' name='td_desc_acao' id='td_desc_acao_${cod_linha}'
                style="padding: 0.25rem; align-content: start;">
            </td>
            <td style="padding: 0.25rem;align-content: start;">
                <select name="sl_usu_frm_edt_acao" id="sl_usu_frm_edt_acao_${cod_linha}">
                    ${let_options_usu}
                </select>
            </td>
            <td name="td_inicia_acao" id="td_inicia_acao_${cod_linha}" align="center" style="align-content: start;padding-top: .5rem;">
                <button style="width: 35px;" value="0" title="Iniciar ação"
                    class="btn btn-rounded btn-space" name='btn_inicia_acao' id='btn_inicia_acao_${cod_linha}' disabled >
                    <i class="fa-solid fa-play" style="color: {{cor_empresa_hex}}" ></i>
                </button>
            </td>
            <td contenteditable='false' style="padding: 0.25rem; align-content: start;" >
                <input type="date" id='dt_prazo_frm_edt_acao_${cod_linha}' name="dt_prazo_frm_edt_acao" style="width: 90px;">
            </td>
            <td contenteditable='true' name='td_observacao' id='td_observacao_${cod_linha}'
                style="padding: 0.25rem;align-content: start;"></td>
            <td align="center" style="align-content: start;">
                <button style="width: 35px;" value="0" title="Salvar/Atualizar ação"
                    class="btn btn-rounded btn-space" name='btn_salvar_acao' id='btn_salvar_acao_${cod_linha}'>
                    <i class="fa-solid fa-check" style="color: {{cor_empresa_hex}}"></i>
                </button>
            </td>
            <td  name="td_conclui_acao" id="td_conclui_acao_${cod_linha}" align="center" style="align-content: start;" >
                <button style="width: 35px;margin-left: 11px;"  class="btn btn-rounded btn-space" value="0"
                    name='btn_concluir_acao' id='btn_concluir_acao_${cod_linha}' title="Concluir ação" disabled>
                        <i class="fa-solid fa-thumbs-up" style="color: {{cor_empresa_hex}}"></i>
                </button>
            </td>

        </tr>`).insertAfter("#btnAddLineAcao");
    }
    else{
        lista_acoes.forEach( acao => {
            let let_habilita_btn = ``;
            let let_edicao_td = `
                contenteditable='true'
            `;
            if(acao.status_edicao_campos == 'nok'){
                let_habilita_btn = `
                    disabled="disabled"
                `;
                let_edicao_td = `
                    contenteditable='false'
                `;
            }

            let let_options_usu = '';
            for(let i=0; i <  let_lista_usuarios.length; i++){
                let let_selected = '';
                if(let_lista_usuarios[i][0] == acao.cod_usu__cod_usu){
                    let_selected = `selected="selected"`;
                }
                let_options_usu += `
                    <option value="${let_lista_usuarios[i][0]}" ${let_selected}>${let_lista_usuarios[i][1]}</option>
                `;
            }
            let let_atrib = `
                <select name="sl_usu_frm_edt_acao" ${let_habilita_btn} id="sl_usu_frm_edt_acao_${acao.cod_atividade}">
                    ${let_options_usu}
                </select>`;
            let let_btn_inicia_acao = ``;
            if(acao.data_ini == null) {
                let_btn_inicia_acao = `
                    <button style="width: 35px;" value="${acao.cod_atividade}" title="Iniciar ação" ${let_habilita_btn}
                        class="btn btn-rounded btn-space" name='btn_inicia_acao' id='btn_inicia_acao_${acao.cod_atividade}'>
                        <i class="fa-solid fa-play" style="color: {{cor_empresa_hex}}"  ></i>
                    </button>
                `;
            } else {
                let_btn_inicia_acao = acao.data_ini.split('-')[2]+'-'+acao.data_ini.split('-')[1]+'-'+acao.data_ini.split('-')[0];
            }

            let let_btn_data_conclusao = ``;
            if( acao.data_ini == null && acao.data_conclusao == null ) {
                let_btn_data_conclusao = `
                   <button style="width: 35px;margin-left: 11px;"  class="btn btn-rounded btn-space"
                        name='btn_concluir_acao' id='btn_concluir_acao_${acao.cod_atividade}' value="${acao.cod_atividade}"
                        title="Concluir ação" disabled>
                            <i class="fa-solid fa-thumbs-up" style="color: {{cor_empresa_hex}}"></i>
                   </button>
                `;
            } else if(acao.data_conclusao == null && acao.data_ini != null) {
                let_btn_data_conclusao = `
                   <button style="width: 35px;margin-left: 11px;"  ${let_habilita_btn} class="btn btn-rounded btn-space" title="Concluir ação"
                        name='btn_concluir_acao' id='btn_concluir_acao_${acao.cod_atividade}' value="${acao.cod_atividade}">
                        <i class="fa-solid fa-thumbs-up" style="color: {{cor_empresa_hex}}"></i>
                   </button>
                `;


            } else {
                let_btn_data_conclusao = acao.data_conclusao.split('-')[2]+'-'+acao.data_conclusao.split('-')[1]+'-'+acao.data_conclusao.split('-')[0];


            }
            let let_edt = ``;
            let let_btn_edt = ``;
            let let_dt_edt = ``;
            if(acao.data_conclusao != null){
                let_edt = `false`;
                let_btn_edt =   `
                    <button style="width: 35px;" value="${acao.cod_atividade}" class="btn btn-rounded btn-space"
                        name='btn_salvar_acao' id='btn_salvar_acao_${acao.cod_atividade}'
                        title="Salvar/Atualziar ação" disabled>
                         <i class="fa-solid fa-pen-to-square" style="color: {{cor_empresa_hex}}"></i>
                    </button>`;
                let_dt_edt = `<input type="date" id='dt_prazo_frm_edt_acao_${acao.cod_atividade}' name="dt_prazo_frm_edt_acao"
                    value="${acao.data_fim}" style="width: 90px;" disabled>`;

                let_atrib = `
                    <select name="sl_usu_frm_edt_tarefa" id="sl_usu_frm_edt_tarefa_${acao.cod_atividade}" disabled="disabled">
                        ${let_options_usu}
                    </select>`;
            } else {
                if(acao.status_edicao_campos == 'nok'){
                    let_edt = `false`;
                }
                 let_btn_edt =
                    `<button style="width: 35px;" value="${acao.cod_atividade}" ${let_habilita_btn} class="btn btn-rounded btn-space"
                        name='btn_salvar_acao' id='btn_salvar_acao_${acao.cod_atividade}' title="Salvar/Atualizar ação">
                        <i class="fa-solid fa-pen-to-square" style="color: {{cor_empresa_hex}}"></i>
                    </button>`;
                 let_dt_edt = `<input type="date" id='dt_prazo_frm_edt_acao_${acao.cod_atividade}' ${let_habilita_btn} style="width: 90px;"
                    name="dt_prazo_frm_edt_acao" value="${acao.data_fim}">
                   `;
            }

            let let_img_status_acao = `
                <i class="fa-solid fa-thumbs-up" style="color:#6495ED!important;" title="Em andamento"></i>
            `;
            if(acao.status_acao == 'Concluída'){
                let_img_status_acao = `
                    <i class="fa-solid fa-thumbs-up" style="color:#3CB371!important;" title="Concluída"></i>
                `;
            } else if(acao.status_acao == 'Atrasada'){
                let_img_status_acao = `
                    <i class="fa-solid fa-thumbs-down" style="color:#FF0000!important;" title="Atrasada"></i>
                `;
            }


            $("#tb_acoes_modal_edt_proj").append(`
               <tr style="background-color: #e9e9e9c4;" name="tr_acao" class='scroll'>
                    <td style="padding: .8rem;font-size: 10px;align-content: start;" align="center">
                            ${let_img_status_acao}
                    </td>
                    <td contenteditable="${let_edt}" name='td_desc_acao' id='td_desc_acao_${acao.cod_atividade}'
                        style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal; align-content: start;">
                            ${acao.desc_atividade}
                    </td>
                    <td contenteditable="${let_edt}" name='td_usu_acao' id='td_usu_acao_${acao.cod_atividade}'
                        style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal;align-content: start;">
                            ${let_atrib}
                    </td>
                    <td name="td_inicia_acao" id="td_inicia_acao_${acao.cod_atividade}" align="center"
                        style="font-size: 10px;align-content: start;padding-top: .5rem;">
                            ${let_btn_inicia_acao}
                    </td>
                    <td style="padding: 0.25rem; align-content: start;" >
                        ${let_dt_edt}
                    </td>
                    <td contenteditable="${let_edt}" name='td_observacao' id='td_observacao_${acao.cod_atividade}'
                        style="padding: 0.25rem; width: 50px; word-break: break-all; white-space: normal;align-content: start;">
                           ${acao.observacao}
                    </td>
                    <td align="center" style="align-content: start; padding-top: .5rem;">
                        ${let_btn_edt}
                    </td>
                    <td name="td_conclui_acao" id="td_conclui_acao_${acao.cod_atividade}" align="center"
                        style="font-size: 10px;align-content: start; padding-top: .5rem;">
                            ${let_btn_data_conclusao}
                    </td>

                </tr>
            `);
        });
    }
}


<<<<<<< HEAD

=======
>>>>>>> 9d18ac0cda4dddb6054fec4ce37efde4aa20000f
$(document).on('change', '#cb_usuarios_projeto', function(){
    let let_lista_cod_usuarios = $("#cb_usuarios_projeto").val().toString();
    let let_cod_projeto = $("#hd_cod_projeto").val();

    $.ajax({
        type: 'POST',
        url: '/ti_comitec_app/vincula_usuarios_projeto',
        data: {
            'cod_projeto'  :   let_cod_projeto,
            'lista_cod_usuarios' :   let_lista_cod_usuarios
        },
        success: function (dados) {
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
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
        },
    });
});