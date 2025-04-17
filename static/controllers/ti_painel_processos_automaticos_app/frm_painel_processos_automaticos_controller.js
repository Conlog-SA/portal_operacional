
// Define a função que atualiza a página
function atualizarPagina() {
    if ($('#tabela_processos').length > 0) {
        $("#main_menu").html("");
        $.ajax({
            type: 'GET',
            url: '/ti_painel_processos_automaticos_app/',
            success: function(data) {
                setTimeout(() => {
                    $("#main_menu").html(data);
                }, 1000);
            },
            error: function(request, status, error){
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


  // Define o intervalo de tempo para a função
  // setInterval(atualizarPagina, intervalo);

  if (!navigator.userAgent.includes("Firefox")) {
    setInterval(atualizarPagina, 300000);
  }