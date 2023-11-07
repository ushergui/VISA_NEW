from django.db import models
from cadastros.models import Logradouro, Fiscal
from django.core.validators import MinValueValidator, MaxValueValidator

class Risco(models.Model):
    risco = models.CharField(max_length=45, null=False, blank=False)
    valor_risco = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(15)])

    def __str__(self):
        return f'{self.risco}'

class Contabilidade(models.Model):
    nome_contabilidade = models.CharField(max_length=50, null=False, blank=False)
    telefone1_contabilidade = models.CharField(max_length=15, verbose_name="Telefone", null=True, blank=True)
    telefone2_contabilidade = models.CharField(max_length=15, verbose_name="Telefone 2", null=True, blank=True)
    email_contabilidade = models.EmailField(null=True, blank=True)
    contato_contabilidade = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nome_contabilidade

class Legislacao(models.Model):
    lei = models.CharField(max_length=200, null=False, blank=False)
    
    def __str__(self):
        return f'{self.lei}'

class Cnae(models.Model):
    codigo_cnae = models.CharField(max_length=9, null=False, blank=False)
    descricao_cnae = models.CharField(max_length=250, null=False, blank=False)
    observacoes_cnae = models.CharField(max_length=300, null=True, blank=True)
    CNAE_POPULAR_CHOICES = (
        ("Academia", "Academia"),
        ("Açougue", "Açougue"),
        ("Acupuntura", "Acupuntura"),
        ("Albergue/alojamento/pensão", "Albergue/alojamento/pensão"),
        ("Ambulância", "Ambulância"),
        ("Ambulante", "Ambulante"),
        ("APAE", "APAE"),
        ("Atividade de ensino", "Atividade de ensino"),
        ("Atividade de assistência social", "Atividade de assistência social"),
        ("Bufê", "Bufê"),
        ("Cabeleireiro/manicure/pedicure", "Cabeleireiro/manicure/pedicure"),
        ("Cantina", "Cantina"),
        ("CAPS", "CAPS"),
        ("Clínica de vacinação", "Clínica de vacinação"),
        ("Comércio/transp. de produto para saúde/saneante/cosmético", "Comércio/transp. de produto para saúde/saneante/cosmético"),
        ("Comércio atacadista de alimentos", "Comércio atacadista de alimentos"),
        ("Comércio varejista de alimentos", "Comércio varejista de alimentos"),
        ("Comunidade terapêutica", "Comunidade terapêutica"),
        ("Creche", "Creche"),
        ("Dedetização", "Dedetização"),
        ("Dentista", "Dentista"),
        ("Diagnóstico por imagem", "Diagnóstico por imagem"),
        ("Distribuidora/transportadora de alimentos", "Distribuidora/transportadora de alimentos"),
        ("Drogaria", "Drogaria"),
        ("Endoscopia", "Endoscopia"),
        ("Estética", "Estética"),
        ("Farmácia", "Farmácia"),
        ("Fisioterapia", "Fisioterapia"),
        ("Fonoaudiólogo", "Fonoaudiólogo"),
        ("Funerária", "Funerária"),
        ("Hospital", "Hospital"),
        ("Hotel", "Hotel"),
        ("ILPI", "ILPI"),
        ("Indústria de alimento", "Indústria de alimento"),
        ("Indústria de produto para saúde/saneante/cosmético", "Indústria de produto para saúde/saneante/cosmético"),
        ("Laboratórios", "Laboratórios"),
        ("Lanchonete", "Lanchonete"),
        ("Lavanderia", "Lavanderia"),
        ("Litotripsia", "Litotripsia"),
        ("Medico", "Medico"),
        ("Mercado/supermercado", "Mercado/supermercado"),
        ("Motel", "Motel"),
        ("Nutricionista", "Nutricionista"),
        ("Orfanato", "Orfanato"),
        ("Ótica", "Ótica"),
        ("Outras atividades", "Outras atividades"),
        ("Padaria", "Padaria"),
        ("Peixaria", "Peixaria"),
        ("Perfumaria", "Perfumaria"),
        ("Podologia", "Podologia"),
        ("Práticas integrativas e complementares", "Práticas integrativas e complementares"),
        ("Presídio", "Presídio"),
        ("Prótese dentária", "Prótese dentária"),
        ("Psicólogo", "Psicólogo"),
        ("Restaurante", "Restaurante"),
        ("Saneantes", "Saneantes"),
        ("Tatuador", "Tatuador"),
        ("Terapeuta ocupacional", "Terapeuta ocupacional"),
        ("Urgência e emergência", "Urgência e emergência"),
        ("Veterinário", "Veterinário"),


    )
    cnae_popular = models.CharField(max_length=100, null=True, blank=True, choices=CNAE_POPULAR_CHOICES)
    risco_cnae = models.ForeignKey(Risco, on_delete=models.PROTECT)
    legislacao = models.ManyToManyField(Legislacao, related_name='Legislação')
    alimentos = models.BooleanField(default=False)

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
    cnae_principal = models.ForeignKey(Cnae, on_delete=models.PROTECT, verbose_name='CNAE Principal', related_name='CNAE_Principal', default=96)
    cnae = models.ManyToManyField(Cnae, verbose_name='CNAE(s) Secundário(s)', related_name='CNAE_Secundario', blank=True)
    alvara = models.DateField(null=True, blank=True)
    observacoes = models.CharField(max_length=400, verbose_name="Observações", null=True, blank=True)
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
    
    def get_cnae_max_risco(self):
        return self.cnae.order_by('-risco_cnae__valor_risco').first()

class ProtocoloEmpresa(models.Model):
    numero_protocolo = models.CharField(max_length=12, null=False, verbose_name="Número do protocolo")
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)
    
    MOTIVO_CHOICES = (
        ("1", "Alvará Sanitário Inicial"),    
        ("2", "Renovação do alvará"),    
        ("3", "Verificação de risco - a pedido"),    
        ("4", "Verificação de risco  - busca ativa"),    
        ("5", "Denúncia"),    
        ("6", "Requisição de outros órgãos"),    
        ("7", "Inutilização de produtos"),    
        ("8", "Reinspeção a pedido"),    
        ("9", "Reinspeção expontânea"),    
        ("10", "Busca ativa - sem alvará"),    
        ("11", "Assinatura de livro de ótica"),    
        ("12", "Assinatura de livro de psicotrópicos"),    
        ("13", "Entrega de balanços/notificações de receita"),    
        ("14", "Autorização de eventos"),    
        ("15", "Autorização de ambulantes"),    
        ("17", "Certidão de dispensa"),    
        ("18", "Entrega de documentos"),    
        ("19", "Alteração de dados"),    
        ("20", "Orientações"),    
        ("16", "Outros assuntos"),    
    )
    motivo = models.CharField(max_length=120, null=False, choices=MOTIVO_CHOICES)
    FORMA_CHOICES = (
        ("1", "Presencialmente"),  
        ("7", "Não se aplica"),  
        ("2", "Telefone"),    
        ("3", "Ouvidoria"),    
        ("4", "E-mail"),    
        ("5", "Whatsapp"),    
        ("6", "Rede SIM"),    
            
    )
    forma_de_recebimento = models.CharField(max_length=80, null=False, choices=FORMA_CHOICES, default=1)

    entrada_protocolo = models.DateField(null=False, verbose_name="Data de abertura do protocolo")
    entrada_fiscal = models.DateField(null=True, blank=True, verbose_name="Data de entrega para o fiscal")
    encerramento_protocolo = models.DateField(null=True, blank=True, verbose_name="Data de encerramento")
    STATUS_CHOICES = (
        ("1", "Aguardando escolha/entrega de fiscal (Administrativo)"),    
        ("2", "Aguardando realização de inspeção/ emissão de relatório (Fiscal)"),
        ("3", "Aguardando avaliação/ revisão (Coordenação)"),
        ("4", "Protocolo finalizado"),

    )
    fiscal_responsavel = models.ForeignKey(Fiscal, on_delete=models.PROTECT)
    status_protocolo = models.CharField(max_length=80, null=False, choices=STATUS_CHOICES, default=1,verbose_name="Status")
    observacoes_protocolo = models.CharField(max_length=250, null=True, blank=True, verbose_name="Observações")
    
    class Meta:
        ordering = ["empresa"]

    def __str__(self):
        return f"{self.numero_protocolo} - {self.empresa}"

    def save(self, *args, **kwargs):
        self.numero_protocolo = self.numero_protocolo.upper()
        super(ProtocoloEmpresa, self).save(*args, **kwargs)

class Inspecao(models.Model):
    data_inspecao = models.DateField(null=False, verbose_name="Data da Inspeção")
    data_relatorio = models.DateField(null=False, verbose_name="Data do Relatório")
    legislacao = models.TextField(null=True, blank=True, verbose_name="Legislação")
    desenvolvimento = models.TextField(null=True, blank=True, verbose_name="Desenvolvimento")
    inadequacoes = models.TextField(null=True, blank=True, verbose_name="Inadequações")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    conclusao = models.TextField(null=True, blank=True, verbose_name="Conclusão")
    protocolo = models.OneToOneField(ProtocoloEmpresa, on_delete=models.CASCADE)
    vigirisco = models.FileField(upload_to='pdf/', verbose_name="Arquivo do Vigi-Risco")

    class Meta:
        ordering = ["data_inspecao"]

    def __str__(self):
        return f"{self.protocolo.numero_protocolo} - {self.protocolo.empresa}"

class AcaoProdutividade(models.Model):
    codigo_produtividade = models.CharField(max_length=15, unique=True, verbose_name="Código")
    acao = models.CharField(max_length=200, verbose_name="Ação")
    pontos = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Pontos")

    def __str__(self):
        return f"{self.codigo_produtividade} - {self.acao}"
    
class AcaoProdutividadeRel(models.Model):
    produtividade = models.ForeignKey('Produtividade', on_delete=models.CASCADE)
    acao_produtividade = models.ForeignKey(AcaoProdutividade, on_delete=models.CASCADE)
    multiplicador = models.DecimalField(max_digits=5, decimal_places=1)

class Produtividade(models.Model):
    total = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Total de Pontos", null=True, blank=True)
    tempo_gasto = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Tempo gasto")
    mes_produtividade = models.DateField(null=False, blank=False, verbose_name="Mês de Produtividade")
    inspecao = models.OneToOneField(Inspecao, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Inspeção")
    validacao = models.BooleanField(default=False)
    acoes = models.ManyToManyField(AcaoProdutividade, through=AcaoProdutividadeRel)

    def __str__(self):
        return f"Produtividade da inspecao {self.inspecao}"