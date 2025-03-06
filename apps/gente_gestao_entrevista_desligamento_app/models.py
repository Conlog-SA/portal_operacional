import io

from django.db import models
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class Secao_Entrevista_Desligamento(models.Model):
    cod_secao = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    descricao = models.CharField(max_length=80, blank=False, null=False)
    status = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos_secoes'

class Pergunta_Entrevista_Desligamento(models.Model):
    cod_pergunta = models.AutoField(primary_key=True, editable=False, blank=False, auto_created=True)
    descricao = models.CharField(max_length=250, blank=False, null=False)
    cod_secao = models.IntegerField(blank=False, null=False)
    tipo_resposta = models.IntegerField(blank=False, null=False) #1 - Muito satisfeito a Muito insatisfeito, 2 - Sempre a Nunca, 3 - Sim ou Não, 4 - Livre
    status = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos_perguntas'

class Respostas_Entrevista_Desligamento(models.Model):
    matricula = models.CharField(max_length=15, blank=False, null=False, primary_key=True)
    cod_pergunta = models.ForeignKey(Pergunta_Entrevista_Desligamento, models.DO_NOTHING, db_column='cod_pergunta', blank=True,
                                         null=True)
    resposta = models.CharField(max_length=2000, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos_respostas'

class Desligamento(models.Model):
    matricula = models.CharField(max_length=15, blank=False, null=False, primary_key=True)
    nome = models.CharField(max_length=100, blank=False, null=False)
    cod_unidade = models.IntegerField(blank=False, null=False)
    unidade = models.CharField(max_length=100, blank=False, null=False)
    data_admissao = models.DateTimeField(null=False, blank=False)
    data_desligamento = models.DateTimeField(null=False, blank=False)
    cargo = models.CharField(max_length=100, blank=False, null=False)
    contato_telefone = models.CharField(max_length=30, blank=False, null=False)
    contato_email = models.CharField(max_length=100, blank=True, null=True)
    data_emissao_link = models.DateTimeField(null=False, blank=False)
    data_preenchimento = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'op_gente_gestao_desligamentos'

class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf'
            )
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Erro Rendering PDF", status=400)