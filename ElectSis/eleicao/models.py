from django.db import models

# Create your models here.

from django.db import models
from cpf_field.models import CPFField
from datetime import date


class Candidato(models.Model):

    cpf = CPFField('cpf', default='000.000.000-00', unique=True)
    nome = models.CharField(verbose_name='Nome Completo', max_length=255, null=False)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    endereco = models.CharField(verbose_name="Endereço", max_length=255, null=False)

    def __str__(self):
        return "{}".format(self.nome)

class Eleicao(models.Model):

    nome = models.CharField(verbose_name="Nome da Eleição", max_length=80, unique=True)
    data_inicial = models.DateField(verbose_name="Data Inicial")
    data_final = models.DateField(verbose_name="Data Final")
    candidatos = models.ManyToManyField(Candidato, blank=True)
    _total_candidatos = None

    def get_status(self):
        hoje = date.today()
        if self.data_inicial > hoje:

            return "em aberto"

        elif self.data_final > hoje:

            return "andamento"

        else:

            return "finalizada"

    def __str__(self):
        return '{}/{}'.format(self.nome, self.pk)


class Voto(models.Model):

    pleito = models.ForeignKey(Eleicao, on_delete=models.CASCADE, default='')
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, default='')
    eleitor = CPFField('cpf', default='000.000.000-00')

    def __str__(self):
        return "{}|{}".format(self.pleito, self.eleitor)
