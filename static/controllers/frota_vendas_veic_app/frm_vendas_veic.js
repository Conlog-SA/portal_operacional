let let_lista_tipo_veic_tab = [];
let let_lista_veic = [];
let let_lista_veic_vendido = [];

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


$(document).on('change', '#sl_tab_preco_veic', function(){
    let let_cod_tab = $(this).val();
    let let_mostra_veic_vendidos = 'S';
    atualiza_tab_veic(let_cod_tab, let_mostra_veic_vendidos);
    /*
    if($("#chk_veic_vendidos").prop('checked') == true){
        let_mostra_veic_vendidos = 'S';
    }
    */
});

$(document).on('change', '#chk_veic_vendidos', function(){
    let let_cod_tab = $("#sl_tab_preco_veic").val();
    let let_mostra_veic_vendidos = 'S';
    /*
    if($(this).prop('checked') == true){
        let_mostra_veic_vendidos = 'S';
    }
    */
    if(let_cod_tab == '' || let_cod_tab == null) {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Tabela de preços não informada. Informe a tabela de preços!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    } else {
        atualiza_tab_veic(let_cod_tab, let_mostra_veic_vendidos);
    }

});


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_abre_modal_edita_dados_veic_tab") {
        let let_indice_veic = $(this).val();

        /* Seta campos com os dados do veículo */
        $("#div_placa").html("<b>Placa</b> " + let_lista_veic[let_indice_veic][1]);
        $("#div_renavam").html("<b>Renavam</b> " + let_lista_veic[let_indice_veic][2]);
        $("#div_tipo_veic").html("<b>Tipo Veículo</b> " + let_lista_veic[let_indice_veic][3]);
        $("#div_ano_veic").html("<b>Ano</b> " + let_lista_veic[let_indice_veic][7]);
        $("#div_marca_benner").html("<b>Marca Benner</b> " + let_lista_veic[let_indice_veic][5]);
        $("#div_modelo_benner").html("<b>Modelo Benner</b> " + let_lista_veic[let_indice_veic][6]);
        $("#div_qtd_eixo").html("<b>Qtd. Eixo</b> " + let_lista_veic[let_indice_veic][4]);
        $("#div_filial").html("<b>Filial</b> " + let_lista_veic[let_indice_veic][8]);



        $("#sl_tipo_veic_tab option").remove();
        for (var i = 0; i < let_lista_tipo_veic_tab.length; i++) {
            let let_cod_tipo_veic = let_lista_tipo_veic_tab[i][0];
            let let_desc_tipo_veic = let_lista_tipo_veic_tab[i][1];
            $("#sl_tipo_veic_tab").append("<option value='"+let_cod_tipo_veic+"'>"+let_desc_tipo_veic+"</option>");

        }
        $("#sl_tipo_veic_tab").val(let_lista_veic[let_indice_veic][18]);
        $("#sl_tipo_veic_tab").selectpicker('refresh');

        $("#div_preco_veic_tab").html('R$' +  let_lista_veic[let_indice_veic][12]);


       let let_data;
        if ( let_lista_veic[let_indice_veic][23] > 0){
            $.ajax({
            type: 'GET',
            url: '/frota_vendas_veic_app/retorna_marcas_modelo_tipo_veic_selecionado',
            data: {
                'tipo_pesq':    'carrega_dados_veic_tab',
                'cod_ano_tabela'   :   let_lista_veic[let_indice_veic][23]
            },
            dataType: 'json',
            success: function (data) {
                $("#sl_marca_veic_tab option").remove();
                data.lista_marcas.forEach( marca => {
                    $("#sl_marca_veic_tab").append("<option value='"+marca.cod_marca_tab_precos+"'>"+marca.desc_marca+"</option>");
                });
                $("#sl_marca_veic_tab").val(let_lista_veic[let_indice_veic][20]);
                $("#sl_marca_veic_tab").selectpicker('refresh');

                $("#sl_modelo_veic_tab option").remove();
                data.lista_modelos.forEach( modelo =>{
                    $("#sl_modelo_veic_tab").append("<option value='"+modelo.cod_modelo_tab_precos+"'>"+modelo.desc_modelo+"</option>");

                });
                $("#sl_modelo_veic_tab").val(let_lista_veic[let_indice_veic][21]);
                $("#sl_modelo_veic_tab").selectpicker('refresh');

                $("#sl_ano_veic_tab option").remove();
                data.lista_anos.forEach( ano =>{
                    $("#sl_ano_veic_tab").append("<option value='"+ano.cod_ano_modelo_tab+"'>"+ano.ano+"</option>");

                });
                $("#sl_ano_veic_tab").val(let_lista_veic[let_indice_veic][23]);
                $("#sl_ano_veic_tab").selectpicker('refresh');

                $("#txt_cod_modelo_veic_tab").val(let_lista_veic[let_indice_veic][19]);

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

        $("#btn_confirma_marca_modelo_tab").val(let_lista_veic[let_indice_veic][22]);
        $("#modal_edita_dados_veic_tab").show();

    }
    else if (let_nome_btn == "btn_abre_modal_edita_dados_veic_vendidos_tab") {
        let let_indice_veic = $(this).val();

        /* Seta campos com os dados do veículo */
        $("#div_placa").html("<b>Placa</b> " + let_lista_veic_vendido[let_indice_veic][1]);
        $("#div_renavam").html("<b>Renavam</b> " + let_lista_veic_vendido[let_indice_veic][2]);
        $("#div_tipo_veic").html("<b>Tipo Veículo</b> " + let_lista_veic_vendido[let_indice_veic][3]);
        $("#div_ano_veic").html("<b>Ano</b> " + let_lista_veic_vendido[let_indice_veic][7]);
        $("#div_marca_benner").html("<b>Marca Benner</b> " + let_lista_veic_vendido[let_indice_veic][5]);
        $("#div_modelo_benner").html("<b>Modelo Benner</b> " + let_lista_veic_vendido[let_indice_veic][6]);
        $("#div_qtd_eixo").html("<b>Qtd. Eixo</b> " + let_lista_veic_vendido[let_indice_veic][4]);
        $("#div_filial").html("<b>Filial</b> " + let_lista_veic_vendido[let_indice_veic][8]);



        $("#sl_tipo_veic_tab option").remove();
        for (var i = 0; i < let_lista_tipo_veic_tab.length; i++) {
            let let_cod_tipo_veic = let_lista_tipo_veic_tab[i][0];
            let let_desc_tipo_veic = let_lista_tipo_veic_tab[i][1];
            $("#sl_tipo_veic_tab").append("<option value='"+let_cod_tipo_veic+"'>"+let_desc_tipo_veic+"</option>");

        }
        $("#sl_tipo_veic_tab").val(let_lista_veic_vendido[let_indice_veic][22]);
        $("#sl_tipo_veic_tab").selectpicker('refresh');

        $("#div_preco_veic_tab").html('R$' +  let_lista_veic_vendido[let_indice_veic][14]);


       let let_data;
        if ( let_lista_veic_vendido[let_indice_veic][27] > 0){
            $.ajax({
            type: 'GET',
            url: '/frota_vendas_veic_app/retorna_marcas_modelo_tipo_veic_selecionado',
            data: {
                'tipo_pesq':    'carrega_dados_veic_tab',
                'cod_ano_tabela'   :   let_lista_veic_vendido[let_indice_veic][27]
            },
            dataType: 'json',
            success: function (data) {
                $("#sl_marca_veic_tab option").remove();
                data.lista_marcas.forEach( marca => {
                    $("#sl_marca_veic_tab").append("<option value='"+marca.cod_marca_tab_precos+"'>"+marca.desc_marca+"</option>");
                });
                $("#sl_marca_veic_tab").val(let_lista_veic_vendido[let_indice_veic][24]);
                $("#sl_marca_veic_tab").selectpicker('refresh');

                $("#sl_modelo_veic_tab option").remove();
                data.lista_modelos.forEach( modelo =>{
                    $("#sl_modelo_veic_tab").append("<option value='"+modelo.cod_modelo_tab_precos+"'>"+modelo.desc_modelo+"</option>");

                });
                $("#sl_modelo_veic_tab").val(let_lista_veic_vendido[let_indice_veic][25]);
                $("#sl_modelo_veic_tab").selectpicker('refresh');

                $("#sl_ano_veic_tab option").remove();
                data.lista_anos.forEach( ano =>{
                    $("#sl_ano_veic_tab").append("<option value='"+ano.cod_ano_modelo_tab+"'>"+ano.ano+"</option>");

                });
                $("#sl_ano_veic_tab").val(let_lista_veic_vendido[let_indice_veic][27]);
                $("#sl_ano_veic_tab").selectpicker('refresh');

                $("#txt_cod_modelo_veic_tab").val(let_lista_veic_vendido[let_indice_veic][23]);

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

        $("#btn_confirma_marca_modelo_tab").val(let_lista_veic_vendido[let_indice_veic][26]);
        $("#modal_edita_dados_veic_tab").show();

    }
    else if (let_nome_btn == "btn_fecha_modal_edita_dados_veic_tab") {
        $("#sl_marca_veic_tab").val('');
        $("#sl_marca_veic_tab").selectpicker('refresh');

        $("#sl_modelo_veic_tab").val('');
        $("#sl_modelo_veic_tab").selectpicker('refresh');

        $("#sl_ano_veic_tab").val('');
        $("#sl_ano_veic_tab").selectpicker('refresh');

        $("#txt_cod_modelo_veic_tab").val('');

        $("#modal_edita_dados_veic_tab").hide();

        let let_cod_tab = $("#sl_tab_preco_veic").val();
        let let_mostra_veic_vendidos = 'S';
        /*
        if($("#chk_veic_vendidos").prop('checked') == true){
            let_mostra_veic_vendidos = 'S';
        }
        */
        atualiza_tab_veic(let_cod_tab, let_mostra_veic_vendidos);
    }
    else if (let_nome_btn == 'btn_fechar_modal_edita_dados_veic_tab_sem_atualizar'){
        $("#sl_marca_veic_tab").val('');
        $("#sl_marca_veic_tab").selectpicker('refresh');

        $("#sl_modelo_veic_tab").val('');
        $("#sl_modelo_veic_tab").selectpicker('refresh');

        $("#sl_ano_veic_tab").val('');
        $("#sl_ano_veic_tab").selectpicker('refresh');

        $("#txt_cod_modelo_veic_tab").val('');

        $("#modal_edita_dados_veic_tab").hide();


    }
    else if (let_nome_btn == "btn_confirma_marca_modelo_tab") {
        let let_loader_frm_vincula_veic_tab = document.getElementById("loader_frm_vincula_veic_tab");
        let_loader_frm_vincula_veic_tab.style.display = "flex";

        let let_cod_tab = $("#sl_tab_preco_veic").val();
        let let_cod_veic = let_val_btn;
        let let_cod_ano_modelo_tab = $("#sl_ano_veic_tab").val();
        let let_cod_veic_na_tab = $("#txt_cod_modelo_veic_tab").val();
        let let_cod_modelo = $("#sl_modelo_veic_tab").val();
        $.ajax({
            type: 'POST',
            url: '/frota_vendas_veic_app/vincula_veic_tab_preco',
            data: {
                'cod_tab': let_cod_tab,
                'cod_veic':    let_cod_veic,
                'cod_ano_modelo_tab'   :   let_cod_ano_modelo_tab,
                'cod_veic_na_tab': let_cod_veic_na_tab
            },
            dataType: 'json',
            success: function (data) {
                let_loader_frm_vincula_veic_tab.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                $("#div_preco_veic_tab").html('R$' + data.val_comp_veic);
                $("#txt_cod_modelo_veic_tab").val(data.cod_veic_tab);


                /*
                $("#txt_cod_modelo_veic_tab").val('');

                $("#sl_marca_veic_tab").val('');
                $("#sl_marca_veic_tab").selectpicker('refresh');

                $("#sl_modelo_veic_tab").val('');
                $("#sl_modelo_veic_tab").selectpicker('refresh');

                $("#sl_ano_veic_tab").val('');
                $("#sl_ano_veic_tab").selectpicker('refresh');

                $("#btn_confirma_marca_modelo_tab").val('');

                $("#modal_edita_dados_veic_tab").hide();
                */
            },
            error: function (request, status, error) {
                let_loader_frm_vincula_veic_tab.style.display = "none";
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
    else if (let_nome_btn == 'btn_atualiza_preco_todos_veic') {
        let let_loader_frm_vendas_veic = document.getElementById("loader_frm_vendas_veic");
        let_loader_frm_vendas_veic.style.display = "flex";

        let let_cod_tab_preco = $("#sl_tab_preco_veic").val();
        let let_check_atualiza_veic_vendidos = 'N';
        if($("#chk_atualiza_veic_vendidos").prop('checked') == true){
            let_check_atualiza_veic_vendidos = 'S';
        }
        $.ajax({
            type: 'POST',
            url: '/frota_vendas_veic_app/atualiza_precos_tabela_veiculos',
            data: {
                'cod_tab_preco':    let_cod_tab_preco,
                'check_atualiza_veic_vendidos'   :   let_check_atualiza_veic_vendidos
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

                let_loader_frm_vendas_veic.style.display = "none";
            },
            error: function (request, status, error) {
                loader_frm_vincula_veic_tab.style.display = "none";
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


$(document).on('change', 'select', function(){
    let let_nome_sl = $(this).attr('name');
    let let_id_sl = $(this).attr('id');
    let let_val_sl = $(this).val();
    if(let_nome_sl == 'sl_tipo_veic_tab') {
        let let_loader_frm_vincula_veic_tab = document.getElementById("loader_frm_vincula_veic_tab");
        let_loader_frm_vincula_veic_tab.style.display = "flex";
        $.ajax({
            type: 'GET',
            url: '/frota_vendas_veic_app/retorna_marcas_modelo_tipo_veic_selecionado',
            data: {
                'tipo_pesq':    'carrega_dados_marca',
                'cod_tipo_veic'   :   let_val_sl
            },
            dataType: 'json',
            success: function (data) {
                $("#sl_marca_veic_tab option").remove();
                data.lista_marcas.forEach( marca => {
                    $("#sl_marca_veic_tab").append("<option value='"+marca.cod_marca_tab_precos+"'>"+marca.desc_marca+"</option>");
                });
                $("#sl_marca_veic_tab").val('');
                $("#sl_marca_veic_tab").selectpicker('refresh');

                loader_frm_vincula_veic_tab.style.display = "none";
            },
            error: function (request, status, error) {
                loader_frm_vincula_veic_tab.style.display = "none";
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
    else if(let_nome_sl == 'sl_marca_veic_tab') {
        let let_loader_frm_vincula_veic_tab = document.getElementById("loader_frm_vincula_veic_tab");
        let_loader_frm_vincula_veic_tab.style.display = "flex";
        $.ajax({
            type: 'GET',
            url: '/frota_vendas_veic_app/retorna_marcas_modelo_tipo_veic_selecionado',
            data: {
                'tipo_pesq':    'carrega_dados_modelos',
                'cod_marca_tab'   :   let_val_sl
            },
            dataType: 'json',
            success: function (data) {
                $("#sl_modelo_veic_tab option").remove();
                data.lista_modelos.forEach( modelo => {
                    $("#sl_modelo_veic_tab").append("<option value='"+modelo.cod_modelo_tab_precos+"'>"+modelo.desc_modelo+"</option>");
                });
                $("#sl_modelo_veic_tab").val('');
                $("#sl_modelo_veic_tab").selectpicker('refresh');

                let_loader_frm_vincula_veic_tab.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_frm_vincula_veic_tab.style.display = "none";
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
    else if(let_nome_sl == 'sl_modelo_veic_tab') {
        let let_loader_frm_vincula_veic_tab = document.getElementById("loader_frm_vincula_veic_tab");
        let_loader_frm_vincula_veic_tab.style.display = "flex";
        $.ajax({
            type: 'GET',
            url: '/frota_vendas_veic_app/retorna_marcas_modelo_tipo_veic_selecionado',
            data: {
                'tipo_pesq':    'carrega_dados_anos',
                'cod_modelo_tab'   :   let_val_sl
            },
            dataType: 'json',
            success: function (data) {
                $("#sl_ano_veic_tab option").remove();
                data.lista_anos.forEach( ano => {
                    $("#sl_ano_veic_tab").append("<option value='"+ano.cod_ano_modelo_tab+"'>"+ano.ano+"</option>");
                });
                $("#sl_ano_veic_tab").selectpicker('refresh');

                let_loader_frm_vincula_veic_tab.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_frm_vincula_veic_tab.style.display = "none";
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



function atualiza_tab_veic(cod_tab, mostra_veic_vendidos){
    let let_loader_frm_vendas_veic = document.getElementById("loader_frm_vendas_veic");
    let_loader_frm_vendas_veic.style.display = "flex";
    $.ajax({
        type: 'POST',
        url: '/frota_vendas_veic_app/retorna_placas_benner_vincula_a_tabela_selecionada',
        data: {
            'cod_tab'               :   cod_tab,
            'mostra_veic_vendidos'  :   mostra_veic_vendidos
        },
        dataType: 'json',
        success: function (data) {
            $("#div_comp_atualiza_preco_veic").html('');

            let let_chk_atualiza_veic_vendidos = `
                <label class="col-form-label text-white text-left cursor-pointer" for="chk_atualiza_veic_vendidos">
                    Atualizar os veículos vendidos ?
                    <div class="d-flex flex-column ">
                        <div class="container">
                            <input type="checkbox" class="checkbox" name="chk_atualiza_veic_vendidos"
                            id="chk_atualiza_veic_vendidos">
                            <label class="switch" for="chk_atualiza_veic_vendidos">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>
                </label>

            `;

            let let_btn_atualiza_veic = `
                <button type='button' id="btn_atualiza_preco_todos_veic"
                        name="btn_atualiza_preco_todos_veic"
                        class="btn btn-primary btn-rounded botaoPrincipal" >
                    <i class="fa-solid fa-rotate-right"></i>
                    Atualiza preço de todos veículos
                </button>

            `;

            $("#div_comp_atualiza_preco_veic").html(let_chk_atualiza_veic_vendidos + "&nbsp;&nbsp;" + let_btn_atualiza_veic);
            //$("#div_btn_atualiza_preco_veic").html();


            let_lista_veic = [];
            let_lista_veic_vendido = [];

            //dados.lista_veic_vendas.forEach(veic => {
            for (var i = 0; i < data.lista_veic_vendas.length; i++) {
                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                let let_coluna_marca = `
                    ${data.lista_veic_vendas[i].marca}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendas[i].desc_marca_tab}</span>
                `;
                if(data.lista_veic_vendas[i].marca == data.lista_veic_vendas[i].desc_marca_tab){
                    let_coluna_marca = `
                        <span style="color:#1CB60E">${data.lista_veic_vendas[i].marca}</span>
                    `;
                }

                let let_coluna_modelo = `
                    ${data.lista_veic_vendas[i].modelo}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendas[i].desc_modelo_tab}</span>
                `;
                if(data.lista_veic_vendas[i].modelo == data.lista_veic_vendas[i].desc_modelo_tab){
                    let_coluna_modelo = `
                        <span style="color:#1CB60E">${data.lista_veic_vendas[i].modelo}</span>
                    `;
                }

                let let_coluna_ano = `
                    ${data.lista_veic_vendas[i].ano}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendas[i].ano_tab}</span>
                `;
                if(data.lista_veic_vendas[i].ano == data.lista_veic_vendas[i].ano_tab){
                    let_coluna_ano = `
                        <span style="color:#1CB60E">${data.lista_veic_vendas[i].ano}</span>
                    `;
                }

                let let_perc_venda = `
                    <span style="color:#1CB60E">${data.lista_veic_vendas[i].perc_tab_x_venda}</span>
                `;
                if (data.lista_veic_vendas[i].status_venda == 'NOK'){
                    let_perc_venda = `
                        <span style="color:#F70B0D">${data.lista_veic_vendas[i].perc_tab_x_venda}</span>
                    `;
                }


                let let_btn_abre_modal_edita_dados_veic_tab = `
                    <button type='button' id='btn_abre_modal_edita_dados_veic_tab_${i}'
                            name='btn_abre_modal_edita_dados_veic_tab' value='${i}'
                            class='btn btn-rounded btn-space' title='Associar marca e modelo da tabela de pesquisa'>
                        <i class="fa-solid fa-circle-plus" style="color: #f46424;" ></i>
                    </button>
                `;

                let let_veic = [
                    let_img,
                    /* placa */ data.lista_veic_vendas[i].placa,
                    /* renavam */ data.lista_veic_vendas[i].renavam,
                    /* tipo */ data.lista_veic_vendas[i].tipo,
                    /* eixo */ data.lista_veic_vendas[i].eixo,
                    /* marca */ let_coluna_marca,
                    /* modelo */ let_coluna_modelo,
                    /* ano */ let_coluna_ano,
                    /* filial */ data.lista_veic_vendas[i].filial,
                    /* status_benner */ data.lista_veic_vendas[i].status_benner,
                    /* periodo_pesq */ data.lista_veic_vendas[i].periodo_pesq,
                    /* val_compra */ data.lista_veic_vendas[i].val_compra,
                    /* val_fipe */ data.lista_veic_vendas[i].val_fipe,
                    /* perc. sugerido venda */ data.lista_veic_vendas[i].perc_sug_venda,
                    /* val_sugestao_venda */ data.lista_veic_vendas[i].val_sug_venda,
                    /* tempo parado */ 0,
                    /* idade */ data.lista_veic_vendas[i].idade_veic,
                    let_btn_abre_modal_edita_dados_veic_tab,
                    /* tipo_veic_tab */ data.lista_veic_vendas[i].tipo_veic_tab,
                    /* codigo_veic_tab */ data.lista_veic_vendas[i].codigo_veic_tab,
                    /* marca_tab */ data.lista_veic_vendas[i].marca_tab,
                    /* modelo_tab */ data.lista_veic_vendas[i].modelo_tab,
                    /* cod_veic */ data.lista_veic_vendas[i].cod_veic,
                    /* ano_veic_tab */ data.lista_veic_vendas[i].ano_veic_tab

                ];
                let_lista_veic.push(let_veic);
            }
            $('#tab_veic_vendas').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 10,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_veic,
                "columns": [
                    { title: "" },
                    { title: "Placa" },
                    { title: "Renavam" },
                    { title: "Tipo" },
                    { title: "Eixo" },
                    { title: "Marca Benner" },
                    { title: "Modelo Benner" },
                    { title: "Ano" },
                    { title: "Filial" },
                    { title: "Status Benner" },
                    { title: "Período Pesq." },
                    { title: "R$ Compra" },
                    { title: "R$ Tabela" },
                    { title: "% Sugestão venda" },
                    { title: "R$ Sugestão venda" },
                    { title: "Tempo parado" },
                    { title: "Idade" },
                    { title: "Dados Tabela" },
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

            for (var i = 0; i < data.lista_veic_vendidos.length; i++) {
                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                if(data.lista_veic_vendidos[i].status_venda == 'OK'){
                    let_img =   "<i class='fa-solid fa-arrow-up' style='color: #1CB60E;' title='ACIMA'></i>";
                } else if(data.lista_veic_vendidos[i].status_venda == 'NOK'){
                    let_img =   "<i class='fa-solid fa-arrow-down' style='color: #F70B0D;' title='ABAIXO'></i>";
                }


                let let_coluna_marca = `
                    ${data.lista_veic_vendidos[i].marca}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendidos[i].desc_marca_tab}</span>
                `;
                if(data.lista_veic_vendas[i].marca == data.lista_veic_vendidos[i].desc_marca_tab){
                    let_coluna_marca = `
                        <span style="color:#1CB60E">${data.lista_veic_vendidos[i].marca}</span>
                    `;
                }

                let let_coluna_modelo = `
                    ${data.lista_veic_vendidos[i].modelo}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendidos[i].desc_modelo_tab}</span>
                `;
                if(data.lista_veic_vendas[i].modelo == data.lista_veic_vendidos[i].desc_modelo_tab){
                    let_coluna_modelo = `
                        <span style="color:#1CB60E">${data.lista_veic_vendidos[i].modelo}</span>
                    `;
                }

                let let_coluna_ano = `
                    ${data.lista_veic_vendidos[i].ano}<br>
                    <span style="color:#F70B0D">${data.lista_veic_vendidos[i].ano_tab}</span>
                `;
                if(data.lista_veic_vendidos[i].ano == data.lista_veic_vendidos[i].ano_tab){
                    let_coluna_ano = `
                        <span style="color:#1CB60E">${data.lista_veic_vendidos[i].ano}</span>
                    `;
                }

                let let_perc_venda = `
                    <span style="color:#1CB60E">${data.lista_veic_vendidos[i].perc_tab_x_venda}</span>
                `;
                if (data.lista_veic_vendidos[i].status_venda == 'NOK'){
                    let_perc_venda = `
                        <span style="color:#F70B0D">${data.lista_veic_vendidos[i].perc_tab_x_venda}</span>
                    `;
                }

                let let_btn_abre_modal_edita_dados_veic_tab = `
                    <button type='button' id='btn_abre_modal_edita_dados_veic_vendidos_tab_${i}'
                            name='btn_abre_modal_edita_dados_veic_vendidos_tab' value='${i}'
                            class='btn btn-rounded btn-space' title='Associar marca e modelo da tabela de pesquisa'>
                        <i class="fa-solid fa-circle-plus" style="color: #f46424;" ></i>
                    </button>
                `;

                let let_veic_vendido = [
                    let_img,
                    /* placa */ data.lista_veic_vendidos[i].placa,
                    /* renavam */ data.lista_veic_vendidos[i].renavam,
                    /* tipo */ data.lista_veic_vendidos[i].tipo,
                    /* eixo */ data.lista_veic_vendidos[i].eixo,
                    /* marca */ let_coluna_marca,
                    /* modelo */ let_coluna_modelo,
                    /* ano */ let_coluna_ano,
                    /* filial */ data.lista_veic_vendidos[i].filial,
                    /* status_benner */ data.lista_veic_vendidos[i].status_benner,
                    /* nf_venda */ data.lista_veic_vendidos[i].nf_venda,
                    /* data_venda */ data.lista_veic_vendidos[i].data_venda,
                    /* periodo_pesq */ data.lista_veic_vendidos[i].periodo_pesq,
                    /* val_compra */ data.lista_veic_vendidos[i].val_compra,
                    /* val_fipe */ data.lista_veic_vendidos[i].val_fipe,
                    /* perc. sugerido venda */ data.lista_veic_vendidos[i].perc_sug_venda,
                    /* val_sugestao_venda */ data.lista_veic_vendidos[i].val_sug_venda,
                    /* val_venda */ data.lista_veic_vendidos[i].val_venda,
                    /* % tab venda */ let_perc_venda,
                    /* tempo parado */ 0,
                    /* idade */ data.lista_veic_vendidos[i].idade_veic,
                    let_btn_abre_modal_edita_dados_veic_tab,
                    /* tipo_veic_tab */ data.lista_veic_vendidos[i].tipo_veic_tab,
                    /* codigo_veic_tab */ data.lista_veic_vendidos[i].codigo_veic_tab,
                    /* marca_tab */ data.lista_veic_vendidos[i].marca_tab,
                    /* modelo_tab */ data.lista_veic_vendidos[i].modelo_tab,
                    /* cod_veic */ data.lista_veic_vendidos[i].cod_veic,
                    /* ano_veic_tab */ data.lista_veic_vendidos[i].ano_veic_tab

                ];
                let_lista_veic_vendido.push(let_veic_vendido);

            }
            $('#tab_veic_vendidos').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 10,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_veic_vendido,
                "columns": [
                    { title: "" },
                    { title: "Placa" },
                    { title: "Renavam" },
                    { title: "Tipo" },
                    { title: "Eixo" },
                    { title: "Marca Benner" },
                    { title: "Modelo Benner" },
                    { title: "Ano" },
                    { title: "Filial" },
                    { title: "Status Benner" },
                    { title: "NF venda" },
                    { title: "Data venda" },
                    { title: "Período Pesq." },
                    { title: "R$ Compra" },
                    { title: "R$ Tabela" },
                    { title: "% Sugestão venda" },
                    { title: "R$ Sugestão venda" },
                    { title: "R$ Venda" },
                    { title: "% Venda" },
                    { title: "Tempo parado" },
                    { title: "Idade" },
                    { title: "Dados Tabela" },
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

            $('.selectpicker').selectpicker();
            let_loader_frm_vendas_veic.style.display = "none";

            let_lista_tipo_veic_tab = [];
            data.dic_tipo_veic.forEach( tipo => {
                let let_reg = [
                    tipo.cod_tipo_veic_tab_precos,
                    tipo.desc_tipo_veic
                ];
                let_lista_tipo_veic_tab.push(let_reg);
            });

            let let_lista_modelos = [];
            data.lista_modelos_tab_informados.forEach( modelo => {
                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                let let_marca = `
                    <span style="color:#1CB60E">${modelo.marca_veic}</span>
                `;
                if(modelo.marca_veic != modelo.marca_tab){
                    let_marca += `
                        <br><span style="color:#F70B0D">${modelo.marca_tab}</span>
                    `;
                }

                let let_modelo = `
                    <span style="color:#1CB60E">${modelo.modelo_veic}</span>
                `;
                if(modelo.modelo_veic != modelo.modelo_tab){
                    let_modelo += `
                        <br><span style="color:#F70B0D">${modelo.modelo_tab}</span>
                    `;
                }

                let let_ano = `
                    <span style="color:#1CB60E">${modelo.ano_veic}</span>
                `;
                if(modelo.ano_veic != modelo.ano_tab){
                    let_ano += `
                        <br><span style="color:#F70B0D">${modelo.ano_tab}</span>
                    `;
                }

                let let_reg_modelo = [
                    let_img,
                    let_marca,
                    let_modelo,
                    let_ano,
                    modelo.cod_modelo_tabela,
                    modelo.val_medio_compra_veic,
                    modelo.val_medio_tab_precos,
                    modelo.val_media_venda,
                    modelo.perc_venda_x_tab_preco,
                    modelo.qtd_veic
                ];
                let_lista_modelos.push(let_reg_modelo)
            });
            $('#tab_modelos_tab_vinculados').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 10,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_modelos,
                "columns": [
                    { title: "" },
                    { title: "Marca(Veíc./Tab.)" },
                    { title: "Modelo(Veíc./Tab.)" },
                    { title: "Ano(Veíc./Tab.)" },
                    { title: "Cód. tab." },
                    { title: "R$ média compra" },
                    { title: "R$ média tab." },
                    { title: "R$ média venda" },
                    { title: "% venda x tabela" },
                    { title: "Qtd. veíc." }
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



        },
        error: function (request, status, error) {
            let_loader_frm_vendas_veic.style.display = "none";
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

