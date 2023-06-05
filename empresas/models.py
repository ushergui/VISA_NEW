from django.db import models
from cadastros.models import Logradouro, Fiscal
from django.core.validators import MinValueValidator, MaxValueValidator

class Risco(models.Model):
    risco = models.CharField(max_length=45, null=False, blank=False)
    valor_risco = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(15)])

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

class Legislacao(models.Model):
    lei = models.CharField(max_length=200, null=False, blank=False)
    
    def __str__(self):
        return f'{self.lei}'

class Cnae(models.Model):
    codigo_cnae = models.CharField(max_length=9, null=False, blank=False)
    descricao_cnae = models.CharField(max_length=100, null=False, blank=False)
    observacoes_cnae = models.CharField(max_length=220, null=True, blank=True)
    risco_cnae = models.ForeignKey(Risco, on_delete=models.PROTECT)
    legislacao = models.ManyToManyField(Legislacao, related_name='Legislação')

    def __str__(self):
        return f'{self.codigo_cnae} - {self.descricao_cnae} - {self.risco_cnae}'

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
    cpf_responsavel_legal = models.CharField(max_length=14,null=True, verbose_name="CPF Responsável legal", blank=True) 
    responsavel_tecnico = models.CharField(max_length=60, verbose_name="Responsável Técnico" ,null=True, blank=True)
    cpf_responsavel_tecnico = models.CharField(max_length=14, null=True, verbose_name="CPF Responsável Técnico", blank=True)
    conselho_responsavel_tecnico = models.CharField(max_length=60, verbose_name="Conselho de classe", null=True, blank=True)
    cnae = models.ManyToManyField(Cnae, verbose_name='CNAE')
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
    #STATUSS_CHOICES = (
     #   ("Estabelecimento recebeu fiscalização no ano e recebeu orientações, necessitando de adequações", "Estabelecimento recebeu fiscalização no ano e recebeu orientações, necessitando de adequações"),
     #   ("Estabelecimento recebeu fiscalização no ano e recebeu orientações, atendendo plenamente as regras de boas práticas.", "Estabelecimento recebeu fiscalização no ano e recebeu orientações, atendendo plenamente as regras de boas práticas."),
      #  ("Estabelecimento não recebeu fiscalização no ano.", "Estabelecimento não recebeu fiscalização no ano."),
   # )
    
   # situacao_pdvisa = models.CharField(max_length=150, null=True, blank=True, choices=STATUSS_CHOICES)

    def __str__(self):
        return self.razao

class ProtocoloEmpresa(models.Model):
    numero_protocolo = models.CharField(max_length=12, null=False)
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)
    observacoes_protocolo = models.CharField(max_length=250, null=False)
    STATUS_CHOICES = (
        ("Aguardando escolha/entrega de fiscal", "Aguardando escolha/entrega de fiscal"),    
        ("Aguardando realização de inspeção/ emissão de relatório", "Aguardando realização de inspeção/ emissão de relatório"),
        ("Aguardando avaliação pela coordenação", "Aguardando avaliação pela coordenação"),
        ("Protocolo finalizado", "Protocolo finalizado"),

    )
    status_protocolo = models.CharField(max_length=80, null=False, choices=STATUS_CHOICES)
    MOTIVO_CHOICES = (
        ("Alvará Sanitário Inicial", "Alvará Sanitário Inicial"),    
        ("Renovação do alvará", "Renovação do alvará"),    
        ("Verificação de risco - a pedido", "Verificação de risco - a pedido"),    
        ("Verificação de risco  - busca ativa", "Verificação de risco  - busca ativa"),    
        ("Denúncia", "Denúncia"),    
        ("Requisição de outros órgãos", "Requisição de outros órgãos"),    
        ("Inutilização de produtos", "Inutilização de produtos"),    
        ("Reinspeção a pedido", "Reinspeção a pedido"),    
        ("Reinspeção expontânea", "Reinspeção expontânea"),    
        ("Busca ativa - sem alvará", "Busca ativa - sem alvará"),    
        ("Assinatura de livro de ótica", "Assinatura de livro de ótica"),    
        ("Assinatura de livro de psicotrópicos", "Assinatura de livro de psicotrópicos"),    
        ("Entrega de balanços/notificações de receita", "Entrega de balanços/notificações de receita"),    
        ("Autorização de eventos", "Autorização de eventos"),    
        ("Autorização de ambulantes", "Autorização de ambulantes"),    

    )
    motivo = models.CharField(max_length=120, null=False, choices=MOTIVO_CHOICES)
    FORMA_CHOICES = (
        ("Presencialmente", "Presencialmente"),    
        ("Telefone", "Telefone"),    
        ("Ouvidoria", "Ouvidoria"),    
        ("E-mail", "E-mail"),    
        ("Whatsapp", "Whatsapp"),    
    )
    forma_de_recebimento = models.CharField(max_length=80, null=False, choices=FORMA_CHOICES)
    entrada_protocolo = models.DateField(null=False)
    entrada_fiscal = models.DateField(null=False)
    encerramento_protocolo = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ["empresa"]

    def __str__(self):
        return self.numero_protocolo

    def save(self, *args, **kwargs):
        self.numero_protocolo = self.numero_protocolo.upper()
        super(ProtocoloEmpresa, self).save(*args, **kwargs)