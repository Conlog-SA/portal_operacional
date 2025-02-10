// Define a função que atualiza a página
function atualizarPagina() {
    location.reload(); // Atualiza a página
  }

  // Define o intervalo de tempo (5 minutos = 300000 milissegundos)
  const intervalo = 300000;

  // Define o intervalo de tempo para a função
  // setInterval(atualizarPagina, intervalo);

  if (!navigator.userAgent.includes("Firefox")) {
    setInterval(atualizarPagina, intervalo);
  }