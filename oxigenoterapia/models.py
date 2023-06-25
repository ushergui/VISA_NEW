from django.db import models
from cadastros.models import Logradouro
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Fisioterapeuta(models.Model):
        nome_fisioterapeuta = models.CharField(max_length=100, null=False, verbose_name="Nome completo")

        matricula_fisioterapeuta = models.CharField(max_length=6, null=False)
        NIVEL_CHOICES = (
            ("Fisioterapeuta I", "Fisioterapeuta I"),
            ("Fisioterapeuta II", "Fisioterapeuta II"),
            ("Fisioterapeuta III", "Fisioterapeuta III"),
        )

        nivel_fisioterapeuta = models.CharField(max_length=19, null=False, choices=NIVEL_CHOICES)

        primeiro_nome_fisioterapeuta = models.CharField(max_length=16, null=False)
        crefito = models.CharField(max_length=40, null=False)
        class Meta:
            ordering = ["nome_fisioterapeuta"]

        def __str__(self):
            return self.primeiro_nome_fisioterapeuta

        def save(self, *args, **kwargs):
            self.primeiro_nome_fisioterapeuta = self.primeiro_nome_fisioterapeuta.upper()
            self.nome_fisioterapeuta = self.nome_fisioterapeuta.upper()

            super(Fisioterapeuta, self).save(*args, **kwargs)

class Usf(models.Model):
     nome_fantasia_usf = models.CharField(max_length=70, verbose_name="USF", null=False, blank=False)
     nome_real = models.CharField(max_length=70, verbose_name="Nome completo USF", null=False, blank=False)
     nome_fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.PROTECT)
     def __str__(self):
        return self.nome_fantasia_usf

class Paciente(models.Model):
    prontuario_paciente = models.CharField(max_length=6, verbose_name="Prontuário", null=False, blank=False)
    nome_paciente = models.CharField(max_length=100, verbose_name="Nome", null=False, blank=False)
    nascimento_paciente = models.DateField(null=True, blank=True, verbose_name="Data de nascimento")
    telefone_paciente1 = models.CharField(max_length=20, verbose_name="Telefone 1", null=True, blank=True)
    telefone_paciente2 = models.CharField(max_length=20, verbose_name="Telefone 2", null=True, blank=True)
    logradouro_paciente = models.ForeignKey(Logradouro, on_delete=models.PROTECT)
    numero_paciente=models.CharField(max_length=20, verbose_name="Número", null=False)
    complemento_paciente=models.CharField(max_length=20, verbose_name="Complemento", null=True, blank=True)
    rg_paciente = models.CharField(max_length=20, verbose_name="RG", null=True, blank=True)
    cpf_paciente = models.CharField(max_length=14,null=True, verbose_name="CPF", blank=True) 
    
    usf_paciente = models.ForeignKey(Usf, on_delete=models.PROTECT, verbose_name="USF")

    STATUS_CHOICES = (
    ("ATIVO","ATIVO"),
    ("ÓBITO","ÓBITO"),
    ("ALTA","ALTA"),
    )
    status = models.CharField(null=False, blank=False, max_length=15, verbose_name="Status", choices=STATUS_CHOICES, default="ATIVO")

    data_obito = models.DateField(null=True, blank=True, verbose_name="Em caso de óbito, digite a data")
    data_alta = models.DateField(null=True, blank=True, verbose_name="Em caso de alta, digite a data")
    observacoes_paciente = models.CharField(max_length=200, verbose_name="Observações", null=True, blank=True)

    def __str__(self):
        return self.nome_paciente

@receiver(pre_save, sender=Paciente)
def update_related_status(sender, instance, **kwargs):
    if instance.pk:  # significa que o objeto já existia, então é uma atualização
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.status == "ATIVO" and instance.status in ["ÓBITO", "ALTA"]:  # significa que o status foi alterado de "ATIVO" para "ÓBITO" ou "ALTA"
            # atualiza o status dos objetos Prescricao relacionados
            Prescricao.objects.filter(paciente=instance, status="ATIVO").update(status=instance.status)
            # atualiza o status dos objetos ModoDeUso relacionados
            ModoDeUso.objects.filter(paciente=instance, status="ATIVO").update(status=instance.status)

class Finalidade(models.Model):    
     finalidade = models.CharField(max_length=30, verbose_name="Finalidade")
     AGRUPAMENTO_CHOICES = (
    ("VENTILAÇÃO","VENTILAÇÃO"),
    ("OXIGENOTERAPIA","OXIGENOTERAPIA"),
    )
     agrupamento = models.CharField(max_length=30, verbose_name="Agrupamento", choices=AGRUPAMENTO_CHOICES)
     def __str__(self):
        return self.finalidade

class Equipamento(models.Model):
     nome_equipamento = models.CharField(max_length=50, null=False, verbose_name="Nome do equipamento")
     empresa_equipamento = models.CharField(max_length=50, null=False, verbose_name="Empresa")
     modelo_equipamento = models.CharField(max_length=50, null=False, verbose_name="Modelo")
     finalidade_equipamento = models.ForeignKey(Finalidade, on_delete=models.PROTECT)
     custo_aluguel = models.FloatField(verbose_name="Custo do aluguel", null=True)

     def __str__(self):
            return self.nome_equipamento

class Descartavel(models.Model):
     nome_descartavel = models.CharField(max_length=50, null=False, verbose_name="Nome do descartável")
     finalidade_descartavel = models.ForeignKey(Finalidade, on_delete=models.PROTECT)

     def __str__(self):
            return self.nome_descartavel
     
class Cid(models.Model):
     codigo_doenca = models.CharField(max_length=5, null=False, verbose_name="Código CID")
     nome_doenca = models.CharField(max_length=80, null=False, verbose_name="Nome da doença")

     def __str__(self):
            return f"{self.codigo_doenca} - {self.nome_doenca}"
    
 
class ModoDeUso(models.Model):
    paciente = models.ForeignKey(Paciente, null=False, related_name='Paciente', on_delete=models.PROTECT)
    equipamento = models.ManyToManyField(Equipamento, related_name='Equipamento')
    data_inicio_uso = models.DateField(null=False, blank=False, verbose_name="Data do início do uso")
    TEMPO_USO_CHOICES = (
         ("Contínuo", "Contínuo"),
         ("Noturno", "Noturno"),
         ("Intermitente", "Intermitente"),
         ("Não está utilizando", "Não está utilizando"),
         ("Se necessário", "Se necessário"),
    )
    tempo_de_uso = models.CharField(null=True, blank=True, max_length=25, verbose_name="Tempo de uso", choices=TEMPO_USO_CHOICES)
    cid = models.ForeignKey(Cid, null=False, related_name='CID', on_delete=models.PROTECT)
    litros = models.CharField(null=True, blank=True, max_length=50)
    parametros = models.CharField(null=True, blank=True, max_length=300, verbose_name="Parâmetros")
    STATUS_CHOICES = (
    ("ATIVO","ATIVO"),
    ("ÓBITO","ÓBITO"),
    ("ALTA","ALTA"),
    )
    status = models.CharField(null=False, blank=False, max_length=15, verbose_name="Status", choices=STATUS_CHOICES, default="ATIVO")

    
    def __str__(self):
        data_inicio_uso_formatada = self.data_inicio_uso.strftime('%d/%m/%Y')
        return f"{self.paciente.nome_paciente} - Prescrição de {data_inicio_uso_formatada}"
    

class Prescricao(models.Model):
    paciente = models.ForeignKey(Paciente, null=False, related_name='Nome', on_delete=models.PROTECT)
    equipamento = models.ManyToManyField(Equipamento, related_name='Equipamentos')
    data_inicio_uso = models.DateField(null=False, blank=False, verbose_name="Data do início do uso")
    TEMPO_USO_CHOICES = (
         ("Contínuo", "Contínuo"),
         ("Noturno", "Noturno"),
         ("Intermitente", "Intermitente"),
         ("Não está utilizando", "Não está utilizando"),
         ("Se necessário", "Se necessário"),
    )
    tempo_de_uso = models.CharField(null=True, blank=True, max_length=25, verbose_name="Tempo de uso", choices=TEMPO_USO_CHOICES)
    cid = models.ForeignKey(Cid, null=False, related_name='CID10', on_delete=models.PROTECT)
    litros = models.CharField(null=True, blank=True, max_length=50)
    parametros = models.CharField(null=True, blank=True, max_length=300, verbose_name="Parâmetros")
    STATUS_CHOICES = (
    ("ATIVO","ATIVO"),
    ("ÓBITO","ÓBITO"),
    ("ALTA","ALTA"),
    )
    status = models.CharField(null=False, blank=False, max_length=15, verbose_name="Status", choices=STATUS_CHOICES, default="ATIVO")
    numero_oficio = models.CharField(null=True, blank=True, max_length=15, verbose_name="Número do Ofício")
    data_oficio = models.DateField(null=True, blank=True, verbose_name="Data do Ofício")
    destinatario_oficio = models.CharField(null=True, blank=True, max_length=45, verbose_name="Destinatário")
    
    def __str__(self):
        data_inicio_uso_formatada = self.data_inicio_uso.strftime('%d/%m/%Y')
        return f"{self.paciente.nome_paciente} - Prescrição de {data_inicio_uso_formatada}"


    
class Atendimento(models.Model):
    prescricao = models.ForeignKey(ModoDeUso, on_delete=models.CASCADE, related_name='atendimentos')
    data_atendimento = models.DateField(null=True, blank=True, verbose_name="Data da visita")
    troca_de_filtro = models.BooleanField(null=True, verbose_name="Houve troca de filtro?")
    troca_de_mascara = models.BooleanField(null=True, verbose_name="Houve troca de máscara?")
    relatorio_atendimento = RichTextField(blank=True, null=True, verbose_name="Relatório do atendimento") 
    fisioterapeuta_atendimento = models.ForeignKey(Fisioterapeuta, null=True, related_name="atendimentos", on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Atendimento {self.id} para a prescrição {self.prescricao.id}"