$(document).on('click','.btn-busca-desligamentos' , function(){
    inicio_periodo_desligamentos = $('#data_inicio_pesquisa_desligados').val();
    fim_periodo_desligamentos = $('#data_fim_pesquisa_desligados').val();

    $.ajax({
	        type: 'GET',
	        data: {
                'inicio_periodo_desligamentos'   :   inicio_periodo_desligamentos,
                'fim_periodo_desligamentos'   :   fim_periodo_desligamentos,
            },
            dataType : "html",
	        url: '/gente_gestao_entrevista_desligamento_app/pesquisa_desligamentos',
	        success: function(response) {

            }
    });
});
