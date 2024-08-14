

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

    if (let_nome_btn == "btn_salva_param_rv_rota") {
        let let_cod_filial = $("#sl_filial_param_rv").val();
        let let_dt_ini = $("#dt_ini_vig_param_rv_rota").val();
        let let_dt_fim = $("#dt_fim_vig_param_rv_rota").val();
        let let_cod_cargo = $("#sl_cargo_param_rv_rota").val();
        let let_fator = $("#sl_fator_param_rv_rota").val();
        let let_val_caixa = $("#txt_val_caixa_param_rv_rota").val();
        let let_val_entrega = $("#txt_val_entrega_param_rv_rota").val();
        let let_tipo_recraga = $("#sl_tipo_recarga_param_rv_rota").val();
        let let_val_recarga = $("#txt_val_recarga_param_rv_rota").val();

        let let_loader_princ_frm_params_rv = document.getElementById("loader_princ_frm_params_rv");
        let_loader_princ_frm_params_rv.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/conecta_rv_app/salva_param_rv',
            data: {
                'tipo_param_rv' :   'rota',
                'cod_filial'    :   let_cod_filial,
                'dt_ini'        :   let_dt_ini,
                'dt_fim'        :   let_dt_fim,
                'cod_cargo'     :   let_cod_cargo,
                'fator'         :   let_fator,
                'val_caixa'     :   let_val_caixa.replace(',','.'),
                'val_entrega'   :   let_val_entrega.replace(',','.'),
                'tipo_recraga'  :   let_tipo_recraga,
                'val_recarga'   :   let_val_recarga.replace(',','.')
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
                carrega_tab_param_rv_rota(let_cod_filial);
                let_loader_princ_frm_params_rv.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_princ_frm_params_rv.style.display = "none";
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
    else if (let_nome_btn == "btn_salva_param_rv_van") {
        let let_cod_filial = $("#sl_filial_param_rv").val();
        let let_dt_ini = $("#dt_ini_vig_param_rv_van").val();
        let let_dt_fim = $("#dt_fim_vig_param_rv_van").val();
        let let_cod_cargo = $("#sl_cargo_param_rv_van").val();
        let let_fator = $("#sl_fator_param_rv_van").val();
        let let_val_caixa = $("#txt_val_caixa_param_rv_van").val();
        let let_val_entrega = $("#txt_val_entrega_param_rv_van").val();
        let let_tipo_recraga = $("#sl_tipo_recarga_param_rv_van").val();
        let let_val_recarga = $("#txt_val_recarga_param_rv_van").val();

        let let_loader_princ_frm_params_rv = document.getElementById("loader_princ_frm_params_rv");
        let_loader_princ_frm_params_rv.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/conecta_rv_app/salva_param_rv',
            data: {
                'tipo_param_rv' :   'van',
                'cod_filial'    :   let_cod_filial,
                'dt_ini'        :   let_dt_ini,
                'dt_fim'        :   let_dt_fim,
                'cod_cargo'     :   let_cod_cargo,
                'fator'         :   let_fator,
                'val_caixa'     :   let_val_caixa.replace(',','.'),
                'val_entrega'   :   let_val_entrega.replace(',','.'),
                'tipo_recraga'  :   let_tipo_recraga,
                'val_recarga'   :   let_val_recarga.replace(',','.')
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
                carrega_tab_param_rv_vans(let_cod_filial);
                let_loader_princ_frm_params_rv.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_princ_frm_params_rv.style.display = "none";
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
    else if (let_nome_btn == "btn_salva_param_rv_bonus_devolucao") {
        let let_cod_filial = $("#sl_filial_param_rv").val();
        let let_dt_ini = $("#dt_ini_vig_param_rv_bonus_devolucao").val();
        let let_dt_fim = $("#dt_fim_vig_param_rv_bonus_devolucao").val();
        let let_cod_cargo = $("#sl_cargo_param_rv_bonus_devolucao").val();
        let let_perc_meta = $("#txt_perc_meta_bonus_devolucao").val();
        let let_val_param_bonus_dev = $("#txt_val_param_rv_bonus_devolucao").val();

        let let_loader_princ_frm_params_rv = document.getElementById("loader_princ_frm_params_rv");
        let_loader_princ_frm_params_rv.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/conecta_rv_app/salva_param_rv',
            data: {
                'tipo_param_rv' :   'bonus_dev',
                'cod_filial'    :   let_cod_filial,
                'dt_ini'        :   let_dt_ini,
                'dt_fim'        :   let_dt_fim,
                'cod_cargo'     :   let_cod_cargo,
                'perc_meta'         :   let_perc_meta.replace(',','.'),
                'val_param_bonus_dev'     :   let_val_param_bonus_dev.replace(',','.')
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
                carrega_tab_param_rv_bonus_dev(let_cod_filial);
                let_loader_princ_frm_params_rv.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_princ_frm_params_rv.style.display = "none";
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
    else if (let_nome_btn == "btn_salva_verba_senior_rv") {
        let let_cod_filial = $("#sl_filial_param_rv").val();
        let let_dt_ini = $("#dt_ini_vig_verba_senior_rv").val();
        let let_dt_fim = $("#dt_fim_vig_verba_senior_rv").val();
        let let_cod_tipo_verba = $("#sl_tipo_verba_senior_rv").val();
        let let_cod_verba = $("#txt_cod_verba_senior_rv").val();

        let let_loader_princ_frm_params_rv = document.getElementById("loader_princ_frm_params_rv");
        let_loader_princ_frm_params_rv.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/conecta_rv_app/salva_param_rv',
            data: {
                'tipo_param_rv' :   'verba_senior',
                'cod_filial'    :   let_cod_filial,
                'dt_ini'        :   let_dt_ini,
                'dt_fim'        :   let_dt_fim,
                'cod_tipo_verba'     :   let_cod_tipo_verba,
                'cod_verba'         :   let_cod_verba.replace(',','.')
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
                carrega_tab_param_rv_verbas(let_cod_filial);
                let_loader_princ_frm_params_rv.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_princ_frm_params_rv.style.display = "none";
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

$(document).on('change', '#sl_filial_param_rv', function(){
    let let_cod_filial = $(this).val();
    carrega_tab_param_rv_rota(let_cod_filial);
    carrega_tab_param_rv_vans(let_cod_filial);
    carrega_tab_param_rv_bonus_dev(let_cod_filial);
    carrega_tab_param_rv_verbas(let_cod_filial);
});


function carrega_tab_param_rv_rota(cod_filial){
    $.ajax({
        type: 'GET',
        url: '/conecta_rv_app/tab_param_rv',
        data: {
            'tipo_param_rv'     :   'rota',
            'cod_filial'        :   cod_filial
        },
        dataType: 'json',
        success: function (dados) {
            let let_tab_param = [];
            let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                `;
            dados.lista_params_filial.forEach(params => {
                let let_cargo = 'Motorista';
                if (params.cargo == '2'){
                    let_cargo = 'Ajudante';
                }

                let let_desc_tipo_recarga = 'NA';
                if(params.tipo_recarga == '1') {
                    let_desc_tipo_recarga = 'Fixa';
                } else if(params.tipo_recarga == '2') {
                    let_desc_tipo_recarga = 'Caixa';
                }

                let reg = [
                    let_img,
                    params.data_ini,
                    params.data_fim,
                    let_cargo,
                    params.fator,
                    params.val_caixaria,
                    params.val_entrega,
                    let_desc_tipo_recarga,
                    params.val_recarga
                ];
                let_tab_param.push(reg);

            });
            $("#tab_frm_param_rv_rota").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_tab_param,
                "columns": [
                    { title: "" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Cargo" },
                    { title: "Fator" },
                    { title: "R$/Caixa" },
                    { title: "R$/Entrega" },
                    { title: "Tipo Recarga" },
                    { title: "R$ Recarga" }
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
                } );


        },
        error: function (request, status, error) {
            let_loader_princ_frm_params_rv.style.display = "none";
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

function carrega_tab_param_rv_as(cod_filial){

}

function carrega_tab_param_rv_vans(cod_filial){
    $.ajax({
        type: 'GET',
        url: '/conecta_rv_app/tab_param_rv',
        data: {
            'tipo_param_rv'     :   'vans',
            'cod_filial'        :   cod_filial
        },
        dataType: 'json',
        success: function (dados) {
            let let_tab_param = [];
            let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                `;
            dados.lista_params_filial.forEach(params => {
                let let_cargo = 'Motorista';
                if (params.cargo == '2'){
                    let_cargo = 'Ajudante';
                }

                let let_desc_tipo_recarga = 'NA';
                if(params.tipo_recarga == '1') {
                    let_desc_tipo_recarga = 'Fixa';
                } else if(params.tipo_recarga == '2') {
                    let_desc_tipo_recarga = 'Caixa';
                }

                let reg = [
                    let_img,
                    params.data_ini,
                    params.data_fim,
                    let_cargo,
                    params.fator,
                    params.val_caixaria,
                    params.val_entrega,
                    let_desc_tipo_recarga,
                    params.val_recarga
                ];
                let_tab_param.push(reg);

            });
            $("#tab_frm_param_rv_van").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_tab_param,
                "columns": [
                    { title: "" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Cargo" },
                    { title: "Fator" },
                    { title: "R$/Caixa" },
                    { title: "R$/Entrega" },
                    { title: "Tipo Recarga" },
                    { title: "R$ Recarga" }
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
                } );


        },
        error: function (request, status, error) {
            let_loader_princ_frm_params_rv.style.display = "none";
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

function carrega_tab_param_rv_bonus_dev(cod_filial){
    $.ajax({
        type: 'GET',
        url: '/conecta_rv_app/tab_param_rv',
        data: {
            'tipo_param_rv'     :   'bonus_dev',
            'cod_filial'        :   cod_filial
        },
        dataType: 'json',
        success: function (dados) {
            let let_tab_param = [];
            let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                `;
            dados.lista_params_filial.forEach(params => {
                let let_cargo = 'Motorista';
                if (params.cargo == '2'){
                    let_cargo = 'Ajudante';
                }

                let let_desc_tipo_recarga = 'NA';
                if(params.tipo_recarga == '1') {
                    let_desc_tipo_recarga = 'Fixa';
                } else if(params.tipo_recarga == '2') {
                    let_desc_tipo_recarga = 'Caixa';
                }

                let reg = [
                    let_img,
                    params.data_ini,
                    params.data_fim,
                    let_cargo,
                    params.perc_meta,
                    params.val_bonus_dev
                ];
                let_tab_param.push(reg);

            });
            $("#tab_frm_param_rv_bonus_devolucao").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_tab_param,
                "columns": [
                    { title: "" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Cargo" },
                    { title: "% Meta" },
                    { title: "R$ Bônus" }
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
                } );


        },
        error: function (request, status, error) {
            let_loader_princ_frm_params_rv.style.display = "none";
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

function carrega_tab_param_rv_verbas(cod_filial){
    $.ajax({
        type: 'GET',
        url: '/conecta_rv_app/tab_param_rv',
        data: {
            'tipo_param_rv'     :   'verba_senior',
            'cod_filial'        :   cod_filial
        },
        dataType: 'json',
        success: function (dados) {
            let let_tab_param = [];
            let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                `;
            dados.lista_params_filial.forEach(params => {
                let let_tipo_verba = '';
                if (params.tipo_verba == '1'){
                    let_tipo_verba = 'Rota';
                } else if (params.tipo_verba == '2'){
                    let_tipo_verba = 'AS';
                } else if (params.tipo_verba == '3'){
                    let_tipo_verba = 'Vans';
                } else if (params.tipo_verba == '4'){
                    let_tipo_verba = 'Recarga';
                } else if (params.tipo_verba == '5'){
                    let_tipo_verba = 'Adicional';
                } else if (params.tipo_verba == '6'){
                    let_tipo_verba = 'Bônus';
                }

                let reg = [
                    let_img,
                    params.data_ini,
                    params.data_fim,
                    let_tipo_verba,
                    params.cod_verba
                ];
                let_tab_param.push(reg);

            });
            $("#tab_frm_verba_senior_rv").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_tab_param,
                "columns": [
                    { title: "" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Tipo verba" },
                    { title: "Código verba" }
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
                } );


        },
        error: function (request, status, error) {
            let_loader_princ_frm_params_rv.style.display = "none";
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