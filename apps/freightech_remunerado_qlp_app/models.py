from django.db import models

from apps.estrut_org_app.models import Projeto
from apps.usuario_app.models import Usuario


# Create your models here.

class Cargos_Freightech(models.Model):
    cod_cargo_freightech = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    grupo_cargo = models.CharField(max_length=20, null=False, blank=False)
    desc_cargo = models.CharField(max_length=80, null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_freightech_cargos'


class Relacao_Cargos_Freightech_Senior(models.Model):
    cod_rel_cargo_freightech_senior = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_cargo_freightech = models.ForeignKey(Cargos_Freightech, models.DO_NOTHING, db_column='cod_cargo_freightech',
                                             null=False, blank=False)
    cod_cargo_senior = models.IntegerField(null=False, blank=False)
    desc_cargo_senior = models.CharField(max_length=80, null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_freightech_rel_cargos_freightech_senior'



class Plan_Remunerada_Freightech(models.Model):
    cod_plan_rem_freigh = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    data_arq_imp = models.DateField(auto_now_add=True)
    hora_arq_imp = models.TimeField(auto_now_add=True)
    nome_arq_original = models.CharField(max_length=500, null=True)
    nome_arq_imp = models.CharField(max_length=500, null=True)
    lista_colunas = models.CharField(max_length=500, null=True, blank=True)
    qtd_colunas = models.IntegerField(null=True, blank=True, default=0)
    qtd_registros = models.IntegerField(null=True, blank=True, default=0)
    qtd_importados = models.IntegerField(null=True, blank=True, default=0)
    qtd_atualizados = models.IntegerField(null=True, blank=True, default=0)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    class Meta:
        managed = True
        db_table = 'op_freightech_plan_remuneracao'


class Registros_Plan_Remunerado_Freightech_Rota_Adm(models.Model):
    cod_qlp_rem_rota_adm = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    vigencia = models.DateField(null=False, blank=False)
    quinzena = models.IntegerField(null=False, blank=False, default=0)
    grupo_cargo = models.CharField(max_length=20, null=False, blank=False)
    desc_cargo = models.CharField(max_length=80, null=False, blank=False)
    val_unit_beneficio = models.DecimalField(max_digits=8, decimal_places=2)
    val_unit_encargos = models.DecimalField(max_digits=8, decimal_places=2)
    val_unit_frota_leve = models.DecimalField(max_digits=8, decimal_places=2)
    val_unit_ordenados = models.DecimalField(max_digits=8, decimal_places=2)
    val_unit_telefonia = models.DecimalField(max_digits=8, decimal_places=2)
    val_unit_uniformes = models.DecimalField(max_digits=8, decimal_places=2)
    val_bench_salarios = models.DecimalField(max_digits=8, decimal_places=2)
    qtd_qlp_bench = models.IntegerField(null=False, blank=False, default=0)
    qtd_beneficios = models.IntegerField(null=False, blank=False, default=0)
    qtd_encargos = models.IntegerField(null=False, blank=False, default=0)
    qtd_frota_leve = models.IntegerField(null=False, blank=False, default=0)
    qtd_ordenados = models.IntegerField(null=False, blank=False, default=0)
    qtd_telefonia = models.IntegerField(null=False, blank=False, default=0)
    qtd_uniformes = models.IntegerField(null=False, blank=False, default=0)
    id_reg_plan = models.CharField(max_length=150, blank=True, null=True, default='')
    cod_cargo_freightech = models.ForeignKey(Cargos_Freightech, models.DO_NOTHING, db_column='cod_cargo_freightech',
                                             null=True, blank=True)
    cod_filial_promax = models.CharField(max_length=10, null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    cod_plan_rem_freigh = models.ForeignKey(Plan_Remunerada_Freightech, models.DO_NOTHING,
                                            db_column='cod_plan_rem_freigh', null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_freightech_plan_remuneracao_rota_adm'


class Registros_Plan_Remunerado_Freightech_Rota_Equipe(models.Model):
    cod_qlp_rem_rota_adm = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    vigencia = models.DateField(null=False, blank=False)
    quinzena = models.IntegerField(null=False, blank=False, default=0)
    turno = models.CharField(max_length=20, null=False, blank=False)
    grupo_cargo = models.CharField(max_length=20, null=False, blank=False)
    desc_cargo = models.CharField(max_length=80, null=False, blank=False)
    qtd_dsr = models.IntegerField(null=True, blank=True)
    qtd_horas_extra_fixa = models.IntegerField(null=True, blank=True)
    perc_abs = models.DecimalField(max_digits=8, decimal_places=2)
    perc_encargo_prov = models.DecimalField(max_digits=8, decimal_places=2)
    perc_turn_over = models.DecimalField(max_digits=8, decimal_places=2)
    premiacao_plus = models.DecimalField(max_digits=8, decimal_places=2)
    qtd_total_por_caminhao_ativo = models.DecimalField(max_digits=8, decimal_places=2)
    qtd_por_caminhao = models.DecimalField(max_digits=8, decimal_places=2)
    val_rem_fixa_contra_cheque = models.DecimalField(max_digits=8, decimal_places=2)
    val_total_ordenado = models.DecimalField(max_digits=8, decimal_places=2)
    val_total_remuneracao= models.DecimalField(max_digits=8, decimal_places=2)
    val_total_remuneracao_com_beneficio = models.DecimalField(max_digits=8, decimal_places=2)
    id_reg_plan = models.CharField(max_length=150, blank=True, null=True, default='')
    cod_cargo_freightech = models.ForeignKey(Cargos_Freightech, models.DO_NOTHING, db_column='cod_cargo_freightech',
                                             null=True, blank=True)
    cod_filial_promax = models.CharField(max_length=10, null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    cod_plan_rem_freigh = models.ForeignKey(Plan_Remunerada_Freightech, models.DO_NOTHING,
                                            db_column='cod_plan_rem_freigh', null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_freightech_plan_remuneracao_rota_equipe'


class Registros_Plan_Remunerado_Freightech_Rota_Equipe_Beneficios(models.Model):
    cod_qlp_rem_rota_adm = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_beneficio = models.CharField(max_length=30, null=False, blank=False)
    vigencia = models.DateField(null=False, blank=False)
    quinzena = models.IntegerField(null=False, blank=False, default=0)
    turno = models.CharField(max_length=20, null=False, blank=False)
    desc_cargo = models.CharField(max_length=80, null=False, blank=False)
    val_total_beneficio = models.DecimalField(max_digits=8, decimal_places=2)
    eh_noturna = models.CharField(max_length=1, null=False, blank=False, default='N')
    id_reg_plan = models.CharField(max_length=150, blank=True, null=True, default='')
    cod_cargo_freightech = models.ForeignKey(Cargos_Freightech, models.DO_NOTHING, db_column='cod_cargo_freightech',
                                             null=True, blank=True)
    cod_filial_promax = models.CharField(max_length=10, null=False, blank=False)
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto', null=False, blank=False)
    cod_plan_rem_freigh = models.ForeignKey(Plan_Remunerada_Freightech, models.DO_NOTHING,
                                            db_column='cod_plan_rem_freigh', null=False, blank=False)
    class Meta:
        managed = True
        db_table = 'op_freightech_plan_remuneracao_rota_equipe_beneficios'





