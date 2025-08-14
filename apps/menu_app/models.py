from django.db import models




class Menu(models.Model):
    cod_menu = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    desc_menu = models.CharField(max_length=50)
    status_menu = models.CharField(max_length=1,default='A')
    pai_menu = models.IntegerField(default=0)
    nome_icone = models.CharField(max_length=200, null=True)
    url_menu = models.CharField(max_length=150, default=0)
    '''Tipo de acesso - P(Publico) / R(Restrito)'''
    tipo_acesso = models.CharField(max_length=1,default='R')
    class Meta:
        managed = True
        db_table = 'ger_menus'






