from django.db import models
from cadastros.models import Logradouro
from django.core.validators import MinValueValidator, MaxValueValidator

class Semana(models.Model):
    semana = models.IntegerField(verbose_name="Semana epidemiológica", validators=[MinValueValidator(1), MaxValueValidator(52)], choices=[(i, i) for i in range(1, 53)])
    data_inicio_semana = models.DateField(verbose_name="Início", null=False)
    data_fim_semana = models.DateField(verbose_name="Término", null=False)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(2022),MaxValueValidator(2100)])
    def __str__(self):
        return str(self.semana)

class Notificacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Paciente", null=False, blank=False)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", null=True, blank=True)
    logradouro_paciente = models.ForeignKey(Logradouro, on_delete=models.PROTECT)
    numero_paciente=models.CharField(max_length=20, verbose_name="Número", null=False)
    USF_CHOICES = (
        ("USF Alvorada", "USF Alvorada"),
        ("USF Asilo", "USF Asilo"),
        ("USF Belvedere", "USF Belvedere"),
        ("USF Centro", "USF Centro"),
        ("USF CAIC II", "USF CAIC II"),
        ("USF CAIC III", "USF CAIC III"),
        ("USF Cidade Industrial", "USF Cidade Industrial"),
        ("USF Diamantina", "USF Diamantina"),
        ("EAP Rural", "EAP Rural"),
        ("USF Estação", "USF Estação"),
        ("USF Guardinha", "USF Guardinha"),
        ("USF João XXIII", "USF João XXIII"),
        ("USF Lagoinha", "USF Lagoinha"),
        ("USF Jardim Planalto", "USF Jardim Planalto"),
        ("USF Mediterranee", "USF Mediterranee"),
        ("USF San Genaro", "USF San Genaro"),
        ("USF Santa Maria", "USF Santa Maria"),
        ("USF São Judas", "USF São Judas"),
        ("Unidade de Termópolis", "Unidade de Termópolis"),
        ("USF Veneza", "USF Veneza"),
        ("USF Verona", "USF Verona"),
        ("USF Vila Formosa", "USF Vila Formosa"),
        ("USF Vila Mariana", "USF Vila Mariana"),
    )
    usf = models.CharField(null=True, blank=True, max_length=35, verbose_name="USF", choices=USF_CHOICES)
    data_recebimento = models.DateField(null=False)
    NOTIFICADORA_CHOICES = (
        ("USF Alvorada", "USF Alvorada"),
        ("Ampara", "Ampara"),
        ("USF Asilo", "USF Asilo"),
        ("USF Belvedere", "USF Belvedere"),
        ("USF Centro", "USF Centro"),
        ("USF CAIC II", "USF CAIC II"),
        ("USF CAIC III", "USF CAIC III"),
        ("USF Cidade Industrial", "USF Cidade Industrial"),
        ("USF Diamantina", "USF Diamantina"),
        ("EAP Guardinha", "EAP Guardinha"),
        ("EAP Rural", "EAP Rural"),
        ("USF Estação", "USF Estação"),
        ("Farmácia Ana Terra", "Farmácia Ana Terra"),
        ("USF Guardinha", "USF Guardinha"),
        ("USF João XXIII", "USF João XXIII"),
        ("Laboratório Athena", "Laboratório Athena"),
        ("Laboratório Biolabory", "Laboratório Biolabory"),
        ("Laboratório Hormossul", "Laboratório Hormossul"),
        ("Laboratório JG", "Laboratório JG"),
        ("Laboratório São Lucas", "Laboratório São Lucas"),
        ("Laboratório Vitale", "Laboratório Vitale"),
        ("USF Lagoinha", "USF Lagoinha"),
        ("USF Jardim Planalto", "USF Jardim Planalto"),
        ("USF Mediterranee", "USF Mediterranee"),
        ("USF San Genaro", "USF San Genaro"),
        ("Santa Casa", "Santa Casa"),
        ("USF Santa Maria", "USF Santa Maria"),
        ("USF São Judas", "USF São Judas"),
        ("Unidade de Termópolis", "Unidade de Termópolis"),
        ("Unimed", "Unimed"),
        ("UPA - Unidade de Pronto Atendimento", "UPA - Unidade de Pronto Atendimento"),
        ("USF Veneza", "USF Veneza"),
        ("USF Verona", "USF Verona"),
        ("Vigilância em Saúde", "Vigilância em Saúde"),
        ("USF Vila Formosa", "USF Vila Formosa"),
        ("USF Vila Mariana", "USF Vila Mariana"),
    )
    notificadora = models.CharField(null=False, verbose_name="Unidade notificadora", max_length=50, choices=NOTIFICADORA_CHOICES)
    data_notificacao = models.DateField(verbose_name="Data da notificação", null=False)
    data_inicio_sintomas = models.DateField(verbose_name="Data de início dos sintomas",null=False)
    data_limite_coleta = models.DateField(verbose_name="Data de limite da coleta",null=False)
    semana_epidemiologica = models.ForeignKey(Semana, on_delete=models.PROTECT)
    sinan = models.PositiveIntegerField(verbose_name="SINAN", null=True, blank=True)
    RESULTADO_CHOICES = (
        ("Positivo NS1", "Positivo NS1"),
        ("Positivo sorologia", "Positivo sorologia"),
        ("Negativo NS1", "Negativo NS1"),
        ("Negativo sorologia", "Negativo sorologia"),
        ("Aguardando agendamento", "Aguardando agendamento"),
        ("Aguardando coleta", "Aguardando coleta"),
        ("Aguardando resultado", "Aguardando resultado"),
        ("Faltou", "Faltou"),
        ("Recusou", "Recusou"),
        ("Isolamento viral positivo", "Isolamento viral positivo"),
        ("Isolamento viral negativo", "Isolamento viral negativo"),
        ("Não agendado", "Não agendado"),
    )
    resultado = models.CharField(null=False, max_length=40 ,choices=RESULTADO_CHOICES)
    internacao = models.DateField(null=True, verbose_name="Internação", blank=True)
    obito = models.DateField(null=True, verbose_name="Óbito", blank=True)
    OBITO_CHOICES = (
        ("Óbito confirmado", "Óbito confirmado"),
        ("Óbito em investigação", "Óbito em investigação"),
        ("Óbito descartado", "Óbito descartado"),
    )
    status_obito = models.CharField(max_length=25, null=True, blank=True, verbose_name="Status óbito", choices=OBITO_CHOICES)
    data_agendamento = models.DateField(null=True, verbose_name="Data de agendamento", blank=True)
    observacoes = models.CharField(max_length=200, verbose_name="Observações", null=True, blank=True)
    CLASSIFICACAO_CHOICES = (
        ("Descartado","Descartado"),
        ("Dengue","Dengue"),
        ("Dengue com Sinais de Alarme","Dengue com Sinais de Alarme"),
        ("Dengue Grave","Dengue Grave"),
        ("Chikungunya","Chikungunya"),
    )
    classificacao = models.CharField(max_length=30, null=True, blank=True, verbose_name="Classificação", choices=CLASSIFICACAO_CHOICES)

    EVOLUCAO_CHOICES = (
        ("Cura","Cura"),
        ("Óbito pelo agravo","Óbito pelo agravo"),
        ("Óbito por outras causas","Óbito por outras causas"),
        ("Óbito em investigação","Óbito em investigação"),
        ("Ignorado","Ignorado"),
    )
    evolucao = models.CharField(max_length=30, null=True, blank=True, verbose_name="Evolução do caso", choices=EVOLUCAO_CHOICES)

    MOTIVO_CHOICES = (
        ("Laboratório", "Laboratório"),
        ("Clínico-Epidemiológico", "Clínico-Epidemiológico"),
        ("Em investigação", "Em investigação"),
    )
    motivo_encerramento = models.CharField(max_length=30, null=True, blank=True, verbose_name="Critério de confirmação/descarte", choices=MOTIVO_CHOICES)
    data_encerramento = models.DateField(null=True, verbose_name="Data de encerramento", blank=True)

    @classmethod
    def existe_paciente_logradouro(cls, nome, logradouro_paciente):
        return cls.objects.filter(nome=nome, logradouro_paciente=logradouro_paciente).exists()

    def __str__(self):
        return self.nome

