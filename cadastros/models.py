from django.db import models
from django.contrib.auth.models import User
#Pra deixar cada um ver somente aquilo que cadastrou, exemplo pra usar: Produtividade

# Create your models here.
from django.urls import reverse


class Estado (models.Model):
    nome_estado=models.CharField(max_length=25, verbose_name="Estado")
    sigla_estado=models.CharField(max_length=2, verbose_name="Sigla do Estado")
    #Anotação padrão para informar que é string

    def __str__(self):
        return self.nome_estado
    class Meta:
        ordering = ['nome_estado']

    def save(self, *args, **kwargs):
        self.nome_estado = self.nome_estado.upper()
        self.sigla_estado = self.sigla_estado.upper()
        super(Estado, self).save(*args, **kwargs)


class Cidade (models.Model):
    nome_cidade=models.CharField(max_length=80, verbose_name="Cidade")
    estado=models.ForeignKey(Estado, on_delete=models.PROTECT)

    def __str__(self):
        return "{} - {}".format(self.nome_cidade, self.estado)

    def save(self, *args, **kwargs):
        self.nome_cidade = self.nome_cidade.upper()
        super(Cidade, self).save(*args, **kwargs)
    class Meta:
        ordering = ["nome_cidade"]

class Bairro (models.Model):
    nome_bairro=models.CharField(max_length=70, verbose_name="Bairro")
    cidade=models.ForeignKey(Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return "{} - {}".format(self.nome_bairro, self.cidade)

    def save(self, *args, **kwargs):
        self.nome_bairro = self.nome_bairro.upper()
        super(Bairro, self).save(*args, **kwargs)
    class Meta:
        ordering = ["nome_bairro"]


class Logradouro (models.Model):

    nome_logradouro=models.CharField(max_length=80, verbose_name="Logradouro")
    TIPOS_CHOICES = (
        ("RUA", "RUA"),
        ("AVENIDA", "AVENIDA"),
        ("PRAÇA", "PRAÇA"),
        ("BECO", "BECO"),
        ("ALAMEDA", "ALAMEDA"),
        ("ESTRADA", "ESTRADA"),
        ("LARGO", "LARGO"),
        ("PASSAGEM", "PASSAGEM"),
        ("PASSARELA", "PASSARELA"),
        ("RODOVIA", "RODOVIA"),
        ("SETOR", "SETOR"),
        ("TRAVESSA", "TRAVESSA"),
        ("TREVO", "TREVO"),
        ("ZONA", "ZONA"),
        ("SITIO", "SITIO"),
        ("FAZENDA", "FAZENDA"),
        ("CHACARA", "CHACARA"),
    )
    tipo = models.CharField(max_length=22, null=False, choices=TIPOS_CHOICES)
    bairro=models.ForeignKey(Bairro, on_delete=models.PROTECT)
    cep = models.CharField(max_length=13, verbose_name="CEP")
    def __str__(self):
        return "{} {} - {} - {}".format(self.tipo, self.nome_logradouro, self.bairro, self.cep)
    def save(self, *args, **kwargs):
        self.nome_logradouro = self.nome_logradouro.upper()
        super(Logradouro, self).save(*args, **kwargs)
    class Meta:
        ordering = ["nome_logradouro"]

class Proprietario(models.Model):
    nome_proprietario = models.CharField(max_length=55)
    logradouro_proprietario = models.ForeignKey(Logradouro, on_delete=models.PROTECT)
    numero_proprietario=models.CharField(max_length=20, verbose_name="Número", null=True)
    complemento_proprietario=models.CharField(max_length=40, verbose_name="Complemento", null=True, blank=True)
    nome_coresponsavel_1 = models.CharField(max_length=60,null=True)
    def __str__(self):
        return self.nome_proprietario

    def save(self, *args, **kwargs):
        self.nome_proprietario = self.nome_proprietario.upper()
        self.numero_proprietario = self.numero_proprietario.upper()
        super(Proprietario, self).save(*args, **kwargs)
    class Meta:
        ordering = ["nome_proprietario"]

    @property
    def complemento(self):
        if self.proprietario.complemento_proprietario is not None:
            return self.proprietario.complemento_proprietario


class Terreno(models.Model):
    inscricao = models.CharField(max_length=18, null=False, unique=True, verbose_name="Inscrição imobiliária")
    logradouro_terreno = models.ForeignKey(Logradouro, on_delete=models.PROTECT, verbose_name="Logradouro do terreno", related_name="logradouro_terreno")
    numero_terreno = models.CharField(max_length=20, verbose_name="Número do terreno")
    complemento_terreno = models.CharField(max_length=40, verbose_name="Complemento", null=True, blank=True)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.PROTECT, verbose_name="Proprietário")
    lote = models.CharField(max_length=10, null=False)
    quadra = models.CharField(max_length=8, null=False)
    area = models.FloatField(null=False)
    logradouro_correspondencia = models.ForeignKey(Logradouro, on_delete=models.PROTECT, verbose_name="Endereço de correspondência", related_name="logradouro_correspondencia")
    numero_correspondencia = models.CharField(max_length=20, verbose_name="Número")
    complemento_correspondencia = models.CharField(max_length=40, verbose_name="Complemento", null=True, blank=True)
    TIPO_CHOICES = (
        ("TERRENO", "TERRENO"),
        ("CASA ABANDONADA", "CASA ABANDONADA"),
    )
    tipo_de_imovel = models.CharField(max_length=22, null=False, choices=TIPO_CHOICES)

    @property
    def complemento(self):
        if self.terreno.complemento_terreno is not None:
            return self.terreno.complemento_terreno


    def save(self, *args, **kwargs):
        self.numero_terreno = self.numero_terreno.upper()
        self.lote = self.lote.upper()
        self.quadra = self.quadra.upper()
        self.numero_correspondencia = self.numero_correspondencia.upper()
        super(Terreno, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.inscricao, self.proprietario)
    class Meta:
        ordering = ["inscricao"]

    #class Produtividade(models.Model):
        #descricao = models.CharField(max_length=280, null=False, verbose_name="Descrição")
       # usuario = models.ForeignKey(User, on_delete=models.PROTECT)
       # pdf_teste = models.FileField(upload_to='pdf/')

class Protocolo(models.Model):
    protocolo = models.CharField(max_length=12, null=False)
    SOLICITANTE_CHOICES = (
        ("PESSOA FÍSICA", "PESSOA FÍSICA"),
        ("CORPO DE BOMBEIROS", "CORPO DE BOMBEIROS"),
        ("MINISTÉRIO PÚBLICO", "MINISTÉRIO PÚBLICO"),
        ("PREFEITURA", "PREFEITURA"),
        ("ORDEM JUDICIAL", "ORDEM JUDICIAL"),
        ("OUTRAS INSTITUIÇÕES", "OUTRAS INSTITUIÇÕES"),
        ("VEREADORES", "VEREADORES"),
    )
    solicitante_protocolo = models.CharField(max_length=40, null=False, choices=SOLICITANTE_CHOICES)
    logradouro = models.ForeignKey('Logradouro', on_delete=models.PROTECT, null=False)
    descricao_protocolo = models.CharField(max_length=250, null=False)
    STATUS_CHOICES = (
        ("ABERTO", "ABERTO"),    
        ("PENDENTE", "PENDENTE"),
        ("AGUARDANDO EDITAL", "AGUARDANDO EDITAL"),
        ("AGUARDANDO RETORNO DA AR", "AGUARDANDO RETORNO DA AR"),
        ("FINALIZADO", "FINALIZADO"),
        ("INSPECIONADO", "INSPECIONADO"),
        ("PRAZO DE DEFESA AR", "PRAZO DE DEFESA AR"),
        ("PRAZO DE DEFESA EDITAL", "PRAZO DE DEFESA EDITAL"),
        ("PRAZO PARA JULGAMENTO AR", "PRAZO PARA JULGAMENTO AR"),
        ("PRAZO DE JULGAMENTO EDITAL", "PRAZO DE JULGAMENTO EDITAL"),

    )
    ouvidoria = models.CharField(max_length=10, null=True, blank=True)
    observacoes = models.CharField(max_length=660, null=True, blank=True)
    status_protocolo = models.CharField(max_length=26, null=False, choices=STATUS_CHOICES)
    entrada_protocolo = models.DateField(null=False)
    encerramento_protocolo = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ["protocolo"]
    @property
    def ouvidorias(self):
        if self.ouvidoria is not None:
            return self.ouvidoria;
        else:
            return ""

    def __str__(self):
        return self.protocolo

    def save(self, *args, **kwargs):
        self.protocolo = self.protocolo.upper()
        self.descricao_protocolo = self.descricao_protocolo.upper()

        super(Protocolo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalhes-protocolo', args=[str(self.id)])


class Fiscal(models.Model):
    nome_fiscal = models.CharField(max_length=36, null=False)

    matricula_fiscal = models.CharField(max_length=5, null=False)
    NIVEL_CHOICES = (
        ("Fiscal Sanitário I", "FISCAL SANITÁRIO I"),
        ("Fiscal Sanitário II", "FISCAL SANITÁRIO II"),
    )

    nivel = models.CharField(max_length=19, null=False, choices=NIVEL_CHOICES)

    primeiro_nome = models.CharField(max_length=16, null=False)
    class Meta:
        ordering = ["nome_fiscal"]

    def __str__(self):
        return self.primeiro_nome

    def save(self, *args, **kwargs):
        self.nome_fiscal = self.nome_fiscal.upper()
        self.primeiro_nome = self.primeiro_nome.upper()

        super(Fiscal, self).save(*args, **kwargs)



class Inspecao(models.Model):
    protocolo = models.ForeignKey('Protocolo', on_delete=models.PROTECT, null=False)
    data_inspecao1 = models.DateField(null=False, verbose_name="Data da inspeção")
    horario_inspecao1 = models.TimeField(null=False, verbose_name="Horário de inspeção")
    foto_inspecao_1 = models.FileField(upload_to='fotos/', verbose_name="Foto da inspeção")
    data_relatorio1 = models.DateField(blank=False, verbose_name="Data do relatório da inspeção")
    fiscal = models.ForeignKey('Fiscal', on_delete=models.PROTECT, null=False)
    produtidade_inspecao = models.DateField(null=True, blank=True, verbose_name="Qual o mês (data) da produtividade?")
    LIMPO_CHOICES = (
        ("LIMPO", "LIMPO"),
        ("RAZOAVEL", "RAZOÁVEL"),
    )
    limpo = models.CharField(max_length=15, null=True, blank=True, choices=LIMPO_CHOICES, verbose_name="Está limpo")
    MATO_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    mato = models.CharField(max_length=1, null=True, blank=True, choices=MATO_CHOICES, verbose_name="Mato alto")

    PNEU_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    pneu = models.CharField(max_length=1, null=True, blank=True, choices=PNEU_CHOICES, verbose_name="Pneu(s)")

    ENTULHO_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    entulho = models.CharField(max_length=1, null=True, blank=True, choices=ENTULHO_CHOICES, verbose_name="Entulho(s)")

    MATERIAL_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    material = models.CharField(max_length=1, null=True, blank=True, choices=MATERIAL_CHOICES, verbose_name="Material(is)")

    LIXO_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    lixo = models.CharField(max_length=1, null=True, blank=True, choices=LIXO_CHOICES, verbose_name="Lixo(s)")

    MOVEL_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    movel = models.CharField(max_length=1, null=True, blank=True, choices=MOVEL_CHOICES, verbose_name="Móvel(is)")

    CARCACA_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    carcaca = models.CharField(max_length=1, null=True, blank=True, choices=CARCACA_CHOICES, verbose_name="Carcaça")

    OUTRO_CHOICES = (
        ("", "NÃO"),
        ("X", "SIM"),
    )
    outro = models.CharField(max_length=1, null=True, blank=True, choices=OUTRO_CHOICES, verbose_name="Outros")

    terreno = models.ForeignKey('Terreno', on_delete=models.PROTECT, null=False)
    
    class Meta:
        ordering = ["-id"]


    #def __str__(self):
        #data_inspecao1_formated = self.data_inspecao1.strftime("%d/%m/%Y")
       # return "{} - {}, {}".format(self.protocolo, self.terreno, data_inspecao1_formated)

    def __str__(self):
        data_inspecao1_formated = self.data_inspecao1.strftime("%d/%m/%Y")
        if self.limpo is None:
            start = "TERRENO SUJO"
        else:
            start = "TERRENO LIMPO OU RAZOÁVEL"
        return "{} - {}, {}, {}".format(self.protocolo, self.terreno, data_inspecao1_formated, start)

    @property
    def complemento(self):
        if self.terreno.complemento_terreno is not None:
            return self.terreno.complemento_terreno


    def lixos(self):
        if self.lixo is not None:
            return self.lixo
        else:
            return " "

    def matos(self):
        if self.mato is not None:
            return self.mato
        else:
            return " "

    def entulhos(self):
        if self.entulho is not None:
            return self.entulho
        else:
            return " "

    def materiais(self):
        if self.material is not None:
            return self.material
        else:
            return " "

    def carcacas(self):
        if self.carcaca is not None:
            return self.carcaca
        else:
            return " "
    def pneus(self):
        if self.pneu is not None:
            return self.pneu
        else:
            return " "

    def materiais(self):
        if self.material is not None:
            return self.material
        else:
            return " "

    def outros(self):
        if self.outro is not None:
            return self.outro
        else:
            return " "

    def moveis(self):
        if self.movel is not None:
            return self.movel
        else:
            return " "


class Infracao(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, verbose_name='Inspeção')
    rastreio_infracao = models.CharField(max_length=13, null=True, blank=True, verbose_name="Código de rastreio")
    STATUS_RASTREIO_CHOICES = (
        ("ENVIADO", "ENVIADO"),
        ("ENTREGUE", "ENTREGUE"),
        ("MUDOU-SE", "MUDOU-SE"),
        ("ENDEREÇO INSUFICIENTE", "ENDEREÇO INSUFICIENTE"),
        ("NÃO EXISTE O NÚMERO", "NÃO EXISTE O NÚMERO"),
        ("DESCONHECIDO", "DESCONHECIDO"),
        ("RECUSADO", "RECUSADO"),
        ("OUTROS", "OUTROS"),
        ("NÃO PROCURADO", "NÃO PROCURADO"),
        ("AUSENTE", "AUSENTE"),
        ("FALECIDO", "FALECIDO"),
        ("ENVIADO POR E-MAIL", "ENVIADO POR E-MAIL"),
        ("ENVIADO POR WHATSAPP", "ENVIADO POR WHATSAPP"),
    )

    status_rastreio = models.CharField(null=True, max_length=22, blank=True, choices=STATUS_RASTREIO_CHOICES, verbose_name="Status devolução Correios")
    data_entrega_autuacao = models.DateField(null=True, blank=True, verbose_name="Data da entrega do Auto de infração ou data da publicação no Jornal")
    prazo_defesa = models.DateField(null=True, blank=True, verbose_name="Prazo de defesa")
    nome_recebedor = models.CharField( blank=True,max_length=60, null=True, verbose_name="Quem recebeu?")
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    numero_format_ano = models.CharField(verbose_name='Auto de Infração', max_length=9, null=True, blank=True)
    data_auto = models.DateField(verbose_name='Data do Auto de Infração', null=False, blank=False)

    #Parte do protocolo de defesa
    protocolo_defesa = models.CharField(null=True, max_length=12, blank=True,verbose_name="Protocolo de defesa")
    entrada_protocolo = models.DateField(null=True, blank=True, verbose_name="Data de entrada")
    GRAU_CHOICES = (
        ("PROPRIO", "PROPRIO"),
        ("CORRESPONSAVEL", "CORRESPONSAVEL"),
        ("OUTROS", "OUTROS")
    )
    quem = models.CharField(null=True, blank=True, max_length=100, verbose_name="Nome de quem protocolou")
    grau = models.CharField(null=True, blank=True, max_length=50, verbose_name="Grau de relação", choices=GRAU_CHOICES)
    prazo_manifesto = models.DateField(null=True, blank=True, verbose_name="Prazo de manifesto")

    #Parte da reinspeção
    data_inspecao2 = models.DateField(null=True, blank=True, verbose_name="Data da reinspeção")
    horario_inspecao2 = models.TimeField(null=True, blank=True, verbose_name="Horário de reinspeção")
    foto_inspecao_2 = models.FileField(upload_to='fotos/', blank=True, verbose_name="Foto da reinspeção")
    data_manifesto = models.DateField(blank=True, null=True, verbose_name="Data do manifesto")
    julgamento = models.DateField(blank=True, null=True, verbose_name="Data do julgamento")
    SITUACAO_CHOICES = (
        ("1", "Defendeu e limpou"),
        ("2", "Não defendeu e limpou"),
        ("3", "Não defendeu e não limpou"),
        ("4", "Manifesto e julgamento fora do sistema"),
        ("5", "Defendeu após o prazo e limpou"),
        ("6", "Não recebeu e limpou"),
        ("7", "Edital"),
        ("8", "Não defendeu e não limpou via Edital"),
        ("9", "Não defendeu e limpou via Edital"),
        ("10", "Perda de prazo"),
        ("11", "Erro na identificação"),
        ("12", "Mudança do proprietário no decorrer do processo"),
        ("13", "Não defendeu e limpou (razoável)"),
        ("14", "Defendeu e limpou (razoável)"),
        ("15", "Não defendeu e limpou (razoável) via Edital"),

    )
    situacao = models.CharField(blank=True, null=True, max_length=25, choices=SITUACAO_CHOICES, verbose_name="Situação")
    rastreio_julgamento = models.CharField(max_length=13, null=True, blank=True, verbose_name="Código de rastreio do julgamento")
    status_rastreio_julgamento = models.CharField(null=True, max_length=22, blank=True, choices=STATUS_RASTREIO_CHOICES, verbose_name="Status devolução julgamento")
    email = models.EmailField(max_length=254, null=True, blank=True, verbose_name="Email")
    data_entrega_julgamento = models.DateField(null=True, blank=True, verbose_name="Data da entrega do julgamento")
    produtividade_infracao = models.DateField(null=True, blank=True, verbose_name="Qual o mês (data) da produtividade?")
    produtividade_manifesto = models.DateField(null=True,blank=True, verbose_name="Qual o mês (data) da produtividade do manifesto?")
    
    

    def vrm(self):
        data = self.data_auto
        ano = data.year
        vrmAtual = 0
        if ano == 2022:
            vrmAtual = 2.1972
        if ano == 2023:
            vrmAtual = 2.3589
            
        vrm = self.inspecao.terreno.area * vrmAtual
        return str(f'{round(vrm, 2):.2f}'.replace('.',','))



    def get_sequencial(self):
        data = self.data_auto
        ano = data.year
        infracao = Infracao.objects.filter(
            data_auto__year=ano).last()
        if infracao:
            return infracao.numero + 1
        else:
            return 1
    @property
    def numero_formatado(self):
        data = self.data_auto
        ano = data.year
        return f'{str(self.numero).zfill(4)}/{str(ano)}'



    def save(self, *args, **kwargs):
        if self.numero is None or self.numero == '':
            self.numero = self.get_sequencial()
        if self.numero_format_ano is None:
            self.numero_format_ano = self.numero_formatado

        if self.rastreio_infracao is not None:
            self.rastreio_infracao.upper()
        super(Infracao, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Infrações'


    def __str__(self):
        return f'{self.numero_formatado} - {self.inspecao}'


class FeriadoRecesso(models.Model):
    data = models.DateField(verbose_name="Data")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    tipo = models.CharField(max_length=20, choices=[("FERIADO", "Feriado"), ("RECESSO", "Recesso")], verbose_name="Tipo")

    class Meta:
        verbose_name_plural = 'Feriados e Recessos'

    def __str__(self):
        return f'{self.data} - {self.descricao} - {self.tipo}'
