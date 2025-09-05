from django.db import models

from apps.estrut_org_app.models import Filial


class Colaborador(models.Model):
    cod_colaborador = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    matricula_colaborador = models.IntegerField(blank=True, null=True)
    nome_colaborador = models.CharField(max_length=100, blank=False, null=False)
    #cod_filial = models.IntegerField(blank=False, null=False)
    desc_cargo = models.CharField(max_length=80, blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    validade_cnh = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    '''G(Gestor)/ U(Usuário) / V(Visitante)'''
    perfil_usu = models.CharField(max_length=1, blank=False, null=False)
    setor = models.IntegerField(blank=True, null=True)
    '''1(Ativo)/ 0(Inativo)'''
    situacao = models.IntegerField(blank=True, null=True)
    setor_administrativo = models.IntegerField(blank=False, null=False, default=0)
    cod_empresa = models.IntegerField(blank=False, null=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial', blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'op_safe_colaboradores'
