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
    let let_loader_frm_vendas_veic = document.getElementById("loader_frm_vendas_veic");
    let_loader_frm_vendas_veic.style.display = "flex";
    $.ajax({
        type: 'POST',
        url: '/frota_vendas_veic_app/retorna_placas_benner_vincula_a_tabela_selecionada',
        data: {
            'cod_tab'         :   $(this).val()
        },
        dataType: 'json',
        success: function (dados) {
            let let_lista_veic = [];
            dados.lista_veic_vendas.forEach(veic => {
                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";

                let let_sl_

                let let_veic = [
                    let_img,
                    veic.placa,
                    veic.renavam,
                    veic.tipo,
                    veic.eixo,
                    veic.marca,
                    veic.modelo,
                    veic.ano,
                    veic.tipo_veic_tab,
                    veic.marca_tab,
                    veic.modelo_tab,
                    veic.codigo_veic_tab,
                    veic.filial,
                    veic.status_benner,
                    veic.nf_venda,
                    veic.data_venda,
                    veic.val_venda,
                    veic.periodo_pesq,
                    veic.val_fipe,
                    veic.atualizado_em
                ];
                let_lista_veic.push(let_veic);

            });
            $('#tab_veic_vendas').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 15,
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
                    { title: "Tipo Tab." },
                    { title: "Marca Tab." },
                    { title: "Modelo Tab." },
                    { title: "Cód. Fipe" },
                    { title: "Filial" },
                    { title: "Status Benner" },
                    { title: "NF venda" },
                    { title: "Data venda" },
                    { title: "R$ venda" },
                    { title: "Período Pesq." },
                    { title: "R$ Fipe" },
                    { title: "Atualizado em" }
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
            let_loader_frm_vendas_veic.style.display = "none";

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

});