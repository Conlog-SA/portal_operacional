

const div_menu = document.getElementById('div_foto_colab_menu');
    const fileInputMenu = document.getElementById('file-input-menu');

    // Adiciona evento de clique na div
    div_menu.addEventListener('click', () => {
      fileInputMenu.click(); // Simula o clique no input de arquivo
    });

    // Adiciona evento ao input de arquivo para alterar o fundo da div
    fileInputMenu.addEventListener('change', function (event) {
      const file = event.target.files[0]; // Obtém o arquivo selecionado

      if (file) {
        const reader = new FileReader();

        // Executa quando o arquivo é carregado
        reader.onload = function (e) {
            let let_frm_data = new FormData();
            let_frm_data.append("file", $('#file-input-menu')[0].files[0]);
            let_frm_data.append('transacao', 'update_foto')
            $.ajax({
                type: 'POST',
                enctype: "multipart/form-data; charset=utf-8",
                url: "/utilitarios_assinatura_email_app/carrega_salva_foto_colab",
                data: let_frm_data,
                dataType: 'json',
                processData: false,
                contentType: false,
                cache: false,
                success: function(data){
                    let caminho_foto_server = 'https://operacional.conlogsa.com.br/media/' + data.foto_postada;
                    console.log(data.foto_postada);
                    const timestamp = new Date().getTime();
                    div_menu.style.backgroundImage = `url('${caminho_foto_server}?_=${timestamp}')`;
                    //div_menu.textContent = ''; // Remove o texto da div
                },
                error: function (request, status, error) {
                    let caminho_foto_server = 'https://operacional.conlogsa.com.br/media/fotos/user_default.jpg';
                    div_menu.style.backgroundImage = `url('${caminho_foto_server}?_=${timestamp}')`;
                    //div_menu.textContent = ''; // Remove o texto da div
                    console.log(error);
                }
            });
        };

        reader.readAsDataURL(file); // Lê o arquivo como uma URL base64
      }
    });

/*
function importa_arquivo_server() {
    let let_nome_arquivo_importado = 'https://operacional.conlogsa.com.br/media/fotos/user_default.jpg';
    let let_frm_data = new FormData();
    let_frm_data.append("file", $('input[type=file]')[0].files[0]);
    let_frm_data.append('transacao', 'update_foto')
    $.ajax({
        type: 'POST',
        enctype: "multipart/form-data; charset=utf-8",
        url: "/utilitarios_assinatura_email_app/carrega_salva_foto_colab",
        data: let_frm_data,
        dataType: 'json',
        processData: false,
        contentType: false,
        cache: false,
        success: function(data){
            let_nome_arquivo_importado = data.foto_postada;
            //let_nome_arquivo_importado = 'https://operacional.conlogsa.com.br/media/' + data.foto_postada;


        },
        error: function (request, status, error) {
            console.log(error);
        }
    });

}

*/


document.getElementById('open_btn_menu').addEventListener('click', function (){
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});

document.getElementById('main_menu').addEventListener('mouseup', function (){
    /*document.getElementById('sidebar').classList.toggle('open-sidebar');*/
    let let_side_bar = document.getElementById('sidebar');
    const lista_classes_side_bar = let_side_bar.classList;
    let let_tem_class_open_sidebar = false;
    lista_classes_side_bar.forEach( classe => {
        if( classe == 'open-sidebar') {
            let_tem_class_open_sidebar = true;
        }
    });
    if(let_tem_class_open_sidebar == true){
        let_side_bar.classList.remove('open-sidebar');
    }
});


let let_a_menu = document.querySelectorAll('.link_menu');
let_a_menu.forEach ( link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        let value = link.getAttribute('value');
        let let_i_link = document.getElementById(`i_icon_seta_menu_${value}`);
        const classes_i = let_i_link.classList;
        let let_abre_menu = null;
        classes_i.forEach( classe => {
            if( classe == 'open_menu') {
                let_abre_menu = false;
            } else if( classe == 'fecha_menu'){
                let_abre_menu = true;
            }
        });

        let let_ul_side_sub_menu = document.getElementById(`ul_side_sub_menu_${value}`);
        if(let_abre_menu == true){
            let_i_link.classList.remove('fecha_menu');
            let_i_link.classList.add('open_menu');
            let_ul_side_sub_menu.classList.remove('side_sub_menu_items');
        } else if(let_abre_menu == false) {
            let_i_link.classList.remove('open_menu');
            let_i_link.classList.add('fecha_menu');
            let_ul_side_sub_menu.classList.add('side_sub_menu_items');
        } else {
            let_i_link.classList.add('open_menu');
            let_ul_side_sub_menu.classList.remove('side_sub_menu_items');
        }

    });


});