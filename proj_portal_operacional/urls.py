from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('', include('apps.app_proj_gerencial_v1.urls')),
    path('', include('apps.home_app.urls')),
    path('senior/', include('apps.conecta_senior_app.urls')),
    path('estrut_org_app/', include('apps.estrut_org_app.urls')),
    path('usuario_app/', include('apps.usuario_app.urls')),
    path('menu_app/', include('apps.menu_app.urls')),
    path('frota_importa_2art_app/', include('apps.frota_importa_2art_app.urls')),
    path('plan_controle_fat_2art_terc_app/', include('apps.plan_controle_fat_2art_terc_app.urls')),
    path('contabil_composicao_app/', include('apps.contabil_composicao_app.urls')),
    path('gente_gestao_erros_pagamento_app/', include('apps.gente_gestao_erros_pagamento_app.urls')),
    path('gente_gestao_fluxo_punitivo/', include('apps.gente_gestao_fluxo_punitivo.urls')),
    path('gente_gestao_rem_var_app/', include('apps.gente_gestao_rem_var_app.urls')),
    path('frota_disponibilidade_app/', include('apps.frota_disponibilidade_app.urls')),
    path('suprimentos_tma_app/', include('apps.suprimentos_tma_app.urls')),
    path('suprimentos_rel_filial_comprador_app/', include('apps.suprimentos_rel_filial_comprador_app.urls')),
    path('suprimentos_evolucao_precos_app/', include('apps.suprimentos_evolucao_precos_app.urls')),
    path('plan_controle_folha_pag_analitico_app/', include('apps.plan_controle_folha_pag_analitico_app.urls')),
    path('plan_controle_provisoes_folha_app/', include('apps.plan_controle_provisoes_folha_app.urls')),
    path('frota_disponibilidade_empilhadeira_app/', include('apps.frota_disponibilidade_empilhadeira_app.urls')),
    path('seguranca_5s_app/', include('apps.seguranca_5s_app.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),    
    path('suprimentos_justifica_preco_diesel_app/', include('apps.suprimentos_justifica_preco_diesel_app.urls')),
    path('frota_vpo_app/', include('apps.frota_vpo_app.urls')),
    path('contabil_operacoes_farol_ndd_app/', include('apps.contabil_operacoes_farol_ndd_app.urls')),
    path('cco_sinistro_app/', include('apps.cco_sinistro_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
