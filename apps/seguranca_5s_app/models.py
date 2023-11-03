from django.db import models

class Cadastro_5s(models.Model):
    id_cadastro_5s = models.AutoField(primary_key=True, editable=False)
    data_lancamento = models.DateField()
    matricula_motorista = models.CharField(null=True, blank=True, max_length=30)
    desc_filial = models.CharField(null=True, blank=True, max_length=20)
    placa =  models.CharField(null=True, blank=True, max_length=12)
    nome_avaliador = models.CharField(null=True, blank=True, max_length=20)
    mapa = models.CharField(null=True, blank=True, max_length=20)
    cabine_livre = models.CharField(null=True, blank=True, max_length=4)
    doc_lugar_adequado = models.CharField(null=True, blank=True, max_length=4)
    estofado_bom = models.CharField(null=True, blank=True, max_length=4)
    aparelho_trk_bom = models.CharField(null=True, blank=True, max_length=4)
    baias_bom = models.CharField(null=True, blank=True, max_length=4)
    notas_organizadas = models.CharField(null=True, blank=True, max_length=4)
    chapatex_organizados = models.CharField(null=True, blank=True, max_length=4)
    plast_papel_segregados = models.CharField(null=True, blank=True, max_length=4)
    pallets_bom = models.CharField(null=True, blank=True, max_length=4)
    vasilhames_separados = models.CharField(null=True, blank=True, max_length=4)
    cabine_limpa = models.CharField(null=True, blank=True, max_length=4)
    baias_limpas = models.CharField(null=True, blank=True, max_length=4)
    eqpe_saber_func_limp = models.CharField(null=True, blank=True, max_length=4)
    eqpe_saber_func_s = models.CharField(null=True, blank=True, max_length=4)
    eqpe_saber_func_rotina_aud = models.CharField(null=True, blank=True, max_length=4)
    eqpe_recorda_gaps = models.CharField(null=True, blank=True, max_length=4)
    eqpq_saber_prog_reconhecimento = models.CharField(null=True, blank=True, max_length=4)
    obs = models.CharField(null=True, blank=True, max_length=100)
    ajudante_1 = models.CharField(null=True, blank=True, max_length=50)
    ajudante_2 = models.CharField(null=True, blank=True, max_length=50)
    class Meta:
        managed = True
        db_table = 'op_seguranca_5s'

