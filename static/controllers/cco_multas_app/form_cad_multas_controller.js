$('#frm_pesq_multas').submit(function(event){
    event.preventDefault();
    placa_selecionada = document.getElementById('cb_placa_pesq_multas').value
    $.ajax({
        type: "GET",
        url: "/cco_multas_app/pesq_reg_multas",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            placa_selecionada : placa_selecionada,
            tipoPesquisaMulta : 'placa',  
        },
        success: function(data) {
            let linhasTabelaMultas = []
            data.linhasTabela.forEach(linha => {
                desc_projeto = linha.desc_projeto
                dt_receb_notificacao = linha.dt_receb_notificacao
                placa_multa = linha.placa_multa
                cod_tipo_multa_reg_antt = linha.cod_tipo_multa_reg_antt
                local_auto = linha.local_auto
                dt_auto = linha.dt_auto
                ai_num_auto = linha.ai_num_auto
                orgao_exp = linha.orgao_exp
                status = linha.status
                nome_condutor =  linha.nome_condutor
                editar = 'Editar'
                excluir = 'Excluir'

                linhaTabela = [desc_projeto, dt_receb_notificacao, placa_multa, cod_tipo_multa_reg_antt, local_auto, dt_auto, ai_num_auto, orgao_exp, status, nome_condutor, editar, excluir]
                linhasTabelaMultas.push(linhaTabela)

            })
            $('#table_registro_multas').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":linhasTabelaMultas,
                "columns": [
                    { title: "Projeto" },
                    { title: "Dt. Recebimento notificação" },
                    { title: "Placa" },
                    { title: "Tipo de Multa" },
                    { title: "Local de Autuação" },
                    { title: "Dt. da Autuação" },
                    { title: "Nº Auto" },
                    { title: "Orgão" },
                    { title: "Status" },
                    { title: "Nome Condutor" },
                    { title: "Editar" },
                    { title: "Excluir" },
                ],
                "columnDefs": [
                    // { "width": "10%", "targets": 0 },
                    // {"className": "dt-left", "targets": [0]},
                    // {"className": "dt-left", "targets": [1]}
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
    
    
})