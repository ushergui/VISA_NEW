from django.db import models
from cadastros.models import Logradouro
from django.core.validators import MinValueValidator, MaxValueValidator

class Risco(models.Model):
    risco = models.CharField(max_length=45, null=False, blank=False)
    valor_risco = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])

    def __str__(self):
        return f'{self.valor_risco} - {self.risco}'

class Contabilidade(models.Model):
    nome_contabilidade = models.CharField(max_length=40, null=False, blank=False)
    telefone1_contabilidade = models.CharField(max_length=15, verbose_name="Telefone", null=True, blank=True)
    telefone2_contabilidade = models.CharField(max_length=15, verbose_name="Telefone 2", null=True, blank=True)
    email_contabilidade = models.EmailField(null=True, blank=True)
    contato_contabilidade = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.nome_contabilidade

class Cnae(models.Model):
    codigo_cnae = models.CharField(max_length=9, null=False, blank=False)
    descricao = models.CharField(max_length=300, null=False, blank=False)
    risco_cnae = models.ForeignKey(Risco, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.codigo_cnae} - {self.descricao} - {self.risco_cnae}'

class Empresas(models.Model):
    razao = models.CharField(max_length=100, verbose_name="Razão Social", null=False, blank=False)
    nome_fantasia = models.CharField(max_length=70, verbose_name="Nome Fantasia", null=True, blank=True)
    mei = models.BooleanField(verbose_name="MEI", null=False, blank=False)
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ", null=True, blank=True)
    telefone1 = models.CharField(max_length=15, verbose_name="Telefone", null=True, blank=True)
    telefone2 = models.CharField(max_length=15, verbose_name="Telefone 2", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logradouro_empresa = models.ForeignKey(Logradouro, on_delete=models.PROTECT)
    numero_empresa=models.CharField(max_length=20, verbose_name="Número", null=False, blank=False)
    complemento_empresa=models.CharField(max_length=40, verbose_name="Complemento", null=True, blank=True)
    responsavel_legal = models.CharField(max_length=60, verbose_name="Responsável legal", null=False, blank=False)
    rg_responsavel_legal = models.CharField(max_length=20, verbose_name="RG", null=True, blank=True)
    cpf_responsavel_legal = models.CharField(max_length=14,null=True, verbose_name="CPF", blank=True) 
    responsavel_tecnico = models.CharField(max_length=60, verbose_name="Responsável Técnico" ,null=True, blank=True)
    cpf_responsavel_tecnico = models.CharField(max_length=14, null=True, verbose_name="CPF", blank=True)
    conselho_responsavel_tecnico = models.CharField(max_length=60, verbose_name="Conselho de classe", null=True, blank=True)
    cnae = models.ManyToManyField(Cnae, related_name='Cnae')
    alvara = models.DateField(null=True, blank=True)
    observacoes = models.CharField(max_length=200, verbose_name="Observações", null=True, blank=True)
    risco_empresa = models.ForeignKey(Risco, on_delete=models.PROTECT)
    contabilidade = models.ForeignKey(Contabilidade, on_delete=models.PROTECT)
    STATUS_CHOICES = (
        ("ATIVA", "ATIVA"),
        ("BAIXADA", "BAIXADA"),
        ("DISPENSADA", "DISPENSADA"),
    )
    status_funcionamento = models.CharField(max_length=20, null=False, blank=False, choices=STATUS_CHOICES)

    def __str__(self):
        return self.razao

"""RISCO_CHOICES = (
        ("Nível de risco I - Dispensada", "Nível de risco I - Dispensada"),
        ("Nível de risco I - Sujeito a visa", "Nível de risco I - Sujeito a visa"),
        ("Nível de risco I MEI - Sujeito a visa", "Nível de risco I MEI - Sujeito a visa"),
        ("Nível de risco II - Médio risco", "Nível de risco II - Médio risco"),
        ("Nível de risco II MEI Médio risco", "Nível de risco II MEI Médio risco"),
        ("Nível de risco II MEI Médio risco", "Nível de risco II MEI Médio risco"),
        ("Nível de risco II MEI Médio risco", "Nível de risco II MEI Médio risco"),
    )
    RISCOS_CHOICES = (
        ("1", "Nível de risco I - Não exerce"),
        ("2", "Nível de risco I - Não sujeito"),
        ("3", "Nível de risco I - Sujeito"),
        ("4", "Nível de risco II"),
        ("5", "Alto risco"),
    )
    
    """