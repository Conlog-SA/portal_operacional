$(document).on('click','.btn-busca-desligamentos' , function(){
    inicio_periodo_desligamentos = $('#data_inicio_pesquisa_desligados').val();
    fim_periodo_desligamentos = $('#data_fim_pesquisa_desligados').val();

    $.ajax({
	        type: 'GET',
	        data: {
                'inicio_periodo_desligamentos'   :   inicio_periodo_desligamentos,
                'fim_periodo_desligamentos'   :   fim_periodo_desligamentos,
            },
            dataType : "json",
	        url: '/gente_gestao_entrevista_desligamento_app/pesquisa_desligamentos',
	        success: function(dados) {
                let_lista_desligamentos_periodo = [];
                console.log(dados);
                dados.lista_desligamentos.forEach(desligamento => {
                    let str_nome_colaborador = "";
                    if (desligamento['existe_resposta'] == true) {
                        str_nome_colaborador = '<a style="color:white" class="abrir-relatorio-desligamento" name="'+desligamento['matricula']+'">'+desligamento['nome']+'</a>';
                    }
                    else {
                        str_nome_colaborador = desligamento['nome'];
                    }

                    if (desligamento['existe_resposta'] == true) {
                        str_link_icon = '<i class="fa-solid fa-check" style="font-size:20px;color:#34B233 !important"></i>'
                    }
                    else {
                        str_link_icon = '<i class="fa-solid fa-paste link-entrevista-desligamento" name="'+desligamento['matricula']+'" style="font-size:20px;color:#f46424"></i>'
                    }
                    let let_dado_desligamento = [
                        desligamento['matricula'],
                        str_nome_colaborador,
                        desligamento['unidade'],
                        new Date(desligamento['data_admissao']).toLocaleString("pt-BR"),
                        new Date(desligamento['data_desligamento']).toLocaleString("pt-BR"),
                        desligamento['cargo'],
                        desligamento['contato_telefone'],
                        desligamento['contato_email'],
                        str_link_icon
                    ];
                    let_lista_desligamentos_periodo.push(let_dado_desligamento);
                });

                $('#tab_desligamentos_periodo').DataTable({
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5',
                ],
                "data":let_lista_desligamentos_periodo,
                    "columns": [
                            { title: "Matricula" },
                            { title: "Nome" },
                            { title: "Unidade" },
                            { title: "Dt Admissão" },
                            { title: "Dt Deslig" },
                            { title: "Cargo" },
                            { title: "Telefone" },
                            { title: "Email" },
                            { title: "Link" },
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
    });
});

$(document).on('click','.link-entrevista-desligamento' , function(){
    name_link_componente = $(this).attr('name');
    matricula_colab = name_link_componente.split('_')[0];

    $.ajax({
	        type: 'GET',
	        data: {
                'matricula_colab'   :   matricula_colab
            },
            dataType : "json",
	        url: '/gente_gestao_entrevista_desligamento_app/gerar_link_entrevista',
	        success: function(dados) {
                let_lista_desligamentos_periodo = [];

                if (dados.token) {
                    // Copiar token para a área de transferência
                    copyToClipboard('127.0.0.1:8000/gente_gestao_entrevista_desligamento_app/frm_entrevista_desligamento?token=' + dados.token);

                    $.gritter.add({
                        title: 'Atenção!',
                        text: 'Link copiado para transferência!',
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }

                console.log(dados);
            }
    });
});

$(document).on('click','.abrir-relatorio-desligamento' , function(){
    let id_desligamento = $(this).attr('name');

    $.ajax({
	        type: 'GET',
	        data: {
                'id_desligamento'   :   id_desligamento
            },
            dataType : "text",
	        url: '/gente_gestao_entrevista_desligamento_app/relatorio_entrevista',
	        success: function(dados) {
	            console.log('teste');
                var file = new Blob([dados], {type: 'application/pdf'});
                console.log(file.size, file.type);
                var fileURL = URL.createObjectURL(file);
                console.log(fileURL);
                window.open(fileURL, '_blank');
            }
    });
});

function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
            .catch(err => {
                console.error('Falha na API Clipboard: ', err);
                fallbackCopyToClipboard(text);
            });
    }
}