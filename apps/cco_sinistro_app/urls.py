from django.urls import path

from . import views

urlpatterns = [
   path('cadastro_sinistros', views.Form_Cad_Sinistros.as_view(),
      name='cadastro_sinistros'),
   path('pesq_reg_sinistros', views.Form_Pesq_Cad_Sinistros.as_view(),
      name='pesq_reg_sinistros'),
   path('cadastro_sinistros_cargas', views.Form_Cad_Sinistros_cargas.as_view(),
      name='cadastro_sinistros_cargas'),       
   path('cadastro_sinistros_eqp', views.Form_cad_equipamentos_veiculos.as_view(),
      name='cadastro_sinistros_eqp'),
   path('atualiza_cb_placa_pesq_sinistros_carga', views.Comp_Placas_View.as_view(),
      name='atualiza_cb_placa_pesq_sinistros_carga'),
   path('exclui_registro_sinistro/<int:pk>/', views.Form_Cad_Sinistros.as_view(),
        name='exclui_registro_sinistro'),
   path('edita_cadastro', views.Form_Edita_Cadastros_View.as_view(),
        name='edita_cadastro'),
]
