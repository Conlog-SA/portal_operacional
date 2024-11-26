

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