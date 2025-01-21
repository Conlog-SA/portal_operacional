from django.db import models

from apps.estrut_org_app.models import Filial, Projeto
from apps.menu_app.models import Menu


class Usuario(models.Model):
    cod_usu = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial')
    nome_usu = models.TextField(max_length=50,null=True)
    status_usu = models.TextField(max_length=1,default='A')
    data_desativacao = models.DateField(null=True)
    email_usu = models.TextField(max_length=100,null=True)
    perfil_usu = models.TextField(max_length=30)
    login_usu = models.TextField(max_length=50)
    sala = models.CharField(max_length=3,null=True)
    tipo_colab = models.CharField(max_length=1, null=True, blank=True)
    corporativo = models.TextField(max_length=1,default='N')
    tel = models.TextField(max_length=25, default='00 9 0000 0000', null=True, blank=True)
    caminho_foto = models.TextField(max_length=200, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'ger_usuarios'

class Usu_Menu(models.Model):
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    cod_menu = models.ForeignKey(Menu, models.DO_NOTHING, db_column='cod_menu')
    status_usu_menu = models.CharField(max_length=1, default='A')
    class Meta:
        managed = True
        db_table = 'ger_usu_menu'
        unique_together = (('cod_usu', 'cod_menu'))

class Proj_Usu(models.Model):
    cod_proj_usu = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    cod_projeto = models.ForeignKey(Projeto, models.DO_NOTHING, db_column='cod_projeto')
    data_fim_proj_usu = models.DateField(null=True)
    status_proj_usu = models.CharField(max_length=1,default='S')
    class Meta:
        managed = True
        db_table = 'ger_proj_usu'


class Liberacao_Usuario_Projeto_Benner(models.Model):
    cod_libera_usu_proj = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    handle_benner = models.IntegerField(blank=False, null=False)
    cod_empresa = models.IntegerField(blank=False, null=False)
    desc_proj_benner = models.CharField(max_length=80, blank=False, null=False)
    ativo_app_folha_pagamento = models.CharField(max_length=1, default='S')
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    class Meta:
        managed=True
        db_table = 'op_liberacao_usu_proj_benner'