from django.db import models

from apps.frota_importa_2art_app.models import Registro2Art
from apps.usuario_app.models import Usuario


class RemuracaoVariavel2Art(models.Model):
    cod_2art_rem_var = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    placa_2art_rem_var = models.CharField(max_length=50,null=True)
    mapa_2art_rem_var = models.CharField(max_length=50, null=True)
    entrega_2art_rem_var = models.CharField(max_length=50,null=True)
    carga_atual_2art_rem_var = models.CharField(max_length=50,null=True)
    frota_2art_rem_var = models.CharField(max_length=50,null=True)
    entregas_2art_rem_var = models.CharField(max_length=50, null=True)
    cxcarreg_2art_rem_var = models.CharField(max_length=50, null=True)
    cxentreg_2art_rem_var = models.CharField(max_length=50, null=True)
    hrsai_2art_rem_var = models.CharField(max_length=50, null=True)
    hrentr_2art_rem_var = models.CharField(max_length=50, null=True)
    recarga_2art_rem_var = models.CharField(max_length=50, null=True)
    hrmatinal_2art_rem_var = models.CharField(max_length=50, null=True)
    hrjornadaliq_2art_rem_var = models.CharField(max_length=50, null=True)
    hrmetajornada_2art_rem_var = models.CharField(max_length=50, null=True)
    vlbateujornmot_2art_rem_var = models.CharField(max_length=50, null=True)
    vlnaobateujornmot_2art_rem_var = models.CharField(max_length=50, null=True)
    vlbateujornaju_2art_rem_var = models.CharField(max_length=50, null=True)
    vlnaobateujornaju_2art_rem_var = models.CharField(max_length=50, null=True)
    qtentregascarregrv_2art_rem_var = models.CharField(max_length=50, null=True)
    qtentregasentregrv_2art_rem_var = models.CharField(max_length=50, null=True)
    hrpcfisica_2art_rem_var = models.CharField(max_length=50, null=True)
    hrpcfinanceira_2art_rem_var = models.CharField(max_length=50, null=True)
    cpf_mot_2art_rem_var = models.CharField(max_length=50,null=True)
    cpf_ajud1_2art_rem_var = models.CharField(max_length=50,null=True)
    cpf_ajud2_2art_rem_var = models.CharField(max_length=50,null=True)
    status_bloqueio_2art_rem_var = models.CharField(max_length=50,null=True)
    data_bloqueio_2art_rem_var = models.DateField(null=True)
    status_edicao_2art_rem_var = models.CharField(max_length=50,null=True)
    data_ultima_edicao_2art_rem_var = models.DateField(null=True)
    status_liberacao_2art_rem_var = models.CharField(max_length=50,null=True)
    data_liberacao_2art_rem_var = models.DateField(null=True)
    codfilial_2art_rem_var = models.CharField(max_length=50,null=True)
    cod_usu_liberacao_2art_rem_var = models.ForeignKey(Usuario, models.DO_NOTHING,
                                                       db_column='cod_usu_liberacao_2art_rem_var', null=True, related_name='+')
    cod_reg_2art = models.ForeignKey(Registro2Art, models.DO_NOTHING, db_column='cod_reg_2art')
    class Meta:
        managed = True
        db_table = 'op_gente_gestao_2art_rem_var'
