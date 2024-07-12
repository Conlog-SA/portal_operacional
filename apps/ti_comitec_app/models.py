from django.db import models

from apps.estrut_org_app.models import Empresa, Atividade
from apps.usuario_app.models import Usuario

class Item_Gut(models.Model):
    cod_item_gut = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc = models.CharField(max_length=40, null=False, blank=False)
    peso = models.IntegerField()
    ativo = models.CharField(max_length=1, null=False, blank=False, default='S')
    tipo = models.CharField(max_length=1, null=False, blank=False) #G: Gravidade, U: Urgencia, T: Tendencia
    flag = models.CharField(max_length=300, null=True, blank=True)
    color_flag = models.CharField(max_length=8, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'op_ti_comitec_item_gut'

# Create your models here.
class Ideia(models.Model):
    cod_ideia = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_chamado = models.IntegerField(null=False, blank=False)
    data_lancamento_idea = models.DateField(auto_now_add=True,null=False, blank=False)
    data_nota_gut = models.DateField(null=True, blank=True)
    data_nota_head = models.DateField(null=True, blank=True)
    desc_ideia = models.CharField(max_length=500)
    resumo_ideia = models.CharField(max_length=300)
    val_ganhos = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    val_despesas = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    horas_ganhas = models.IntegerField(blank=True, null=True, default=0)
    obs_usu_owner = models.CharField(max_length=300, null=True, blank=True)
    obs_usu_master = models.CharField(max_length=300, null=True, blank=True)
    cod_status = models.IntegerField() #0 - Ideia, 1 - Projeto
    cod_atividade = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='cod_atividade', null=True, blank=True)
    cod_usu_master = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu_master',
                                       related_name='cod_usu_master', null=True, blank=True)  # usuário executar a ideia
    cod_usu_owner = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu_owner',
                                           related_name='cod_usu_owner', null=True, blank=True) #dono da ideia
    cod_usu_head = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu_head', related_name='cod_usu_head',
                                     null=True, blank=True)
    obs_usu_head = models.CharField(max_length=300, null=True, blank=True)
    nota_head = models.IntegerField(null=True, blank=True, default=0)
    cod_gut_g = models.ForeignKey(Item_Gut, models.DO_NOTHING, db_column='cod_gut_g', related_name='cod_gut_g',
                                  null=True, blank=True)
    cod_gut_u = models.ForeignKey(Item_Gut, models.DO_NOTHING, db_column='cod_gut_u', related_name='cod_gut_u',
                                  null=True, blank=True)
    cod_gut_t = models.ForeignKey(Item_Gut, models.DO_NOTHING, db_column='cod_gut_t', related_name='cod_gut_t',
                                  null=True, blank=True)
    class Meta:
        managed=True
        db_table = 'op_ti_comitec_ideias'






