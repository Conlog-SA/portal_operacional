from django.db import models

from apps.estrut_org_app.models import Projeto
from apps.usuario_app.models import Usuario


class Vagas_adicionais(models.Model):
    cod_vaga_ad = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    qtd_ad_oc = models.IntegerField(blank=False, null=False)
    qtd_ad_conlog = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField(blank=False, null=False)
    mes = models.IntegerField(blank=False, null=False)
    quinzena = models.IntegerField(blank=False, null=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'op_dp_vagas_adicionais'

