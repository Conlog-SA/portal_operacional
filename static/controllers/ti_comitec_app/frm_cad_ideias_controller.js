let let_dic_usu_sessao = null;

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

$(document).ready(function(){
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
        "columnDefs": [
            {"className": "dt-center", "targets": [0,1,2,3,4,5]},
            {"className": "dt-left", "targets": [8,12,13]},
            {"className": "dt-right", "targets": [6,7,9,10,11]}
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
                    Atualizar dados da minha idéia
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
                        Atualizar dados da minha idéia
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
                    Atualizar dados da minha idéia
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
                let_loader_frm_parecer_master_ideias_comitec.style.display = "flex";
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
            <i class="${ideia.flag_gut_g}" style="color:${ideia.color_flag_gut_g}" title="${ideia.nota_gut_g}"></i>
        `;
        let let_flag_gut_u = `
            <i class="${ideia.flag_gut_u}" style="color:${ideia.color_flag_gut_u}" title="${ideia.nota_gut_u}"></i>
        `;
        let let_flag_gut_t = `
            <i class="${ideia.flag_gut_t}" style="color:${ideia.color_flag_gut_t}" title="${ideia.nota_gut_t}"></i>
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
            {"className": "dt-center", "targets": [0,1,2,3,4,5]},
            {"className": "dt-left", "targets": [8,12,13]},
            {"className": "dt-right", "targets": [6,7,9,10,11]}
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
}
