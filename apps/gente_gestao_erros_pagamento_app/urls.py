from django.urls import path

from apps.gente_gestao_erros_pagamento_app import views

urlpatterns = [
    path('erros_pagamento', views.Form_Erros_Pagamento.as_view(), name='erros_pagamento'),
    path('verbas_erros_pagamento', views.Manipulacao_Verbas.as_view(), name='verbas_erros_pagamento'),
    path('lancamento_erros_pagamento', views.Lancamento_Erros_Pagamento.as_view(), name='lancamento_erros_pagamento'),
    path('tabela', views.Tabela_Erros_Pagamentos.as_view(), name='tabela'),
    path('retorna_registro_erros_pagamento', views.Edita_Erros_Pagamento_View.as_view(), name='retorna_registro_erros_pagamento'),
    path('estorna_registro_erros_pagamento', views.Tabela_Erros_Pagamentos.as_view(), name='estorna_registro_erros_pagamento'),
]