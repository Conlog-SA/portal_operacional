from django.db import models
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario
import os
from django.utils import timezone

class Despesas_Carga_Descarga(models.Model):
    id_despesa = models.CharField(primary_key=True, editable=False, max_length=50)
    tipo_despesa = models.IntegerField(blank=False, null=False) #pontual
    entrega = models.CharField(max_length=50, blank=False) #Rota/ AS/ Empurrada
    despesa = models.IntegerField(blank=False, null=False)#serviço
    subcategoria = models.IntegerField(blank=False, null=False)#taxa de descarga
    dt_mapa = models.DateField(null=False, blank=False)
    mapa = models.CharField(max_length=50, null=False)
    placa = models.CharField(max_length=50, null=False)
    cod_promax_cliente = models.IntegerField( blank=False, null=False)
    tipo_descarga = models.IntegerField(blank=False, null=False) # por pallet? caixaria?
    quantidade = models.IntegerField(null=False, blank=False)
    valor_unit = models.DecimalField(max_digits=8, decimal_places=2)
    comprovante = models.FileField(upload_to=lambda instance, filename: instance.caminho_upload_personalizado(filename), blank=False, null=False)
    cod_filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='cod_filial')
    cod_usu = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='cod_usu')
    data_lancamento = models.DateField(null=False, blank=False)
    importado = models.IntegerField(null=False, blank=False) #0 - não importado 1 - importado
    un_venda = models.IntegerField(null=False, blank=False)  # 0 - Não é multi CDD
    modal = models.CharField(max_length=50, blank=False) # Mapas2art LancEmpurrada LancRota/AS

    def caminho_upload_personalizado(self, filename):
        _, extensao = os.path.splitext(filename)
        novo_nome = f"{self.cod_filial.cod_promax}_{self.mapa}_{self.cod_promax_cliente}{extensao}"
        return os.path.join('docs', 'processo_carga_descarga_app',str(self.cod_filial.cod_promax),str(self.mapa),str(self.cod_promax_cliente),novo_nome)

    class Meta():
        managed = True
        db_table = 'op_proc_carga_descarga'

