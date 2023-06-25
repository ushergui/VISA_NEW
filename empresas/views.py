from django.shortcuts import render, redirect, get_object_or_404
from .models import Contabilidade, Cnae, Empresas, Risco, Legislacao, ProtocoloEmpresa, Inspecao, AcaoProdutividade, Produtividade, AcaoProdutividadeRel
from .forms import ContabilidadeForm, CnaeForm, EmpresasForm, RiscoForm, LegislacaoForm, ProtocoloEmpresaForm, InspecaoForm, AcaoProdutividadeForm, ProdutividadeForm, ProdutividadeFormEdit
from django.views import View
from django.db.models import Max
from django.http import JsonResponse
from django.views.generic import TemplateView


# Contabilidade
def listar_contabilidades(request):
    contabilidades = Contabilidade.objects.all()
    return render(request, 'empresas/listar_contabilidades.html', {'contabilidades': contabilidades})

def criar_contabilidade(request):
    form = ContabilidadeForm(request.POST or None)
    titulo = "Cadastro de Contabilidade"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def editar_contabilidade(request, id):
    contabilidade = Contabilidade.objects.get(id=id)
    form = ContabilidadeForm(request.POST or None, instance=contabilidade)
    titulo = "Edição de Contabilidade"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def excluir_contabilidade(request, id):
    contabilidade = Contabilidade.objects.get(id=id)

    if request.method == 'POST':
        contabilidade.delete()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/confirmar_exclusao.html', {'obj': contabilidade})

# Cnae
def listar_cnaes(request):
    cnaes = Cnae.objects.all()
    return render(request, 'empresas/listar_cnaes.html', {'cnaes': cnaes})

def criar_cnae(request):
    form = CnaeForm(request.POST or None)
    titulo = "Cadastrar CNAE"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_cnae(request, id):
    cnae = Cnae.objects.get(id=id)
    form = CnaeForm(request.POST or None, instance=cnae)
    titulo = "Edição de Cnae"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def excluir_cnae(request, id):
    cnae = Cnae.objects.get(id=id)

    if request.method == 'POST':
        cnae.delete()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form-excluir.html', {'obj': cnae})

# Empresas
def listar_empresas(request):
    empresas = Empresas.objects.all()
    return render(request, 'empresas/listar_empresas.html', {'empresas': empresas})

def criar_empresa(request):
    form = EmpresasForm(request.POST or None)
    titulo = "Cadastrar empresa"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_empresas')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    form = EmpresasForm(request.POST or None, instance=empresa)
    titulo = "Edição de empresa"
    botao = "Gravar"
    
    if form.is_valid():
        form.save()
        return redirect('listar_empresas')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def excluir_empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if request.method == 'POST':
        empresa.delete()
        return redirect('listar_empresas')

    return render(request, 'empresas/form-excluir.html', {'obj': empresa})

def detalhe_empresa(request, empresa_id):
    empresa = Empresas.objects.get(id=empresa_id)
    protocolos = ProtocoloEmpresa.objects.filter(empresa=empresa)
    return render(request, 'empresas/detalhe_empresa.html', {'empresa': empresa, 'protocolos': protocolos})

def listar_risco(request):
    riscos = Risco.objects.all()
    return render(request, 'empresas/listar_risco.html', {'riscos': riscos})

def cadastrar_risco(request):
    form = RiscoForm(request.POST or None)
    titulo = "Cadastrar risco"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_risco(request, id):
    risco = get_object_or_404(Risco, id=id)
    form = RiscoForm(request.POST or None, instance=risco)
    titulo = "Editar risco"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def excluir_risco(request, id):
    risco = get_object_or_404(Risco, id=id)

    if request.method == 'POST':
        risco.delete()
        return redirect('listar_risco')

    return render(request, 'empresas/form-excluir.html', {'risco': risco})

class GetRisco(View):
    def get(self, request, *args, **kwargs):
        cnaes = [int(i) for i in request.GET.getlist('cnaes')]
        print(Cnae.objects.filter(id__in=cnaes))
        print(Cnae.objects.filter(id__in=cnaes).values('risco_cnae__valor_risco'))
        max_risco = Cnae.objects.filter(id__in=cnaes).aggregate(Max('risco_cnae__valor_risco'))['risco_cnae__valor_risco__max']
        return JsonResponse({'risco': max_risco})


def listar_legislacao(request):
    legislacao = Legislacao.objects.all()
    return render(request, 'empresas/listar_legislacao.html', {'object_list': legislacao})

def criar_legislacao(request):
    form = LegislacaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Nova Legislação', 'botao': 'Criar'})

def editar_legislacao(request, id):
    legislacao = Legislacao.objects.get(id=id)
    form = LegislacaoForm(request.POST or None, instance=legislacao)

    if form.is_valid():
        form.save()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Editar Legislação', 'botao': 'Editar'})

def excluir_legislacao(request, id):
    legislacao = get_object_or_404(Legislacao, id=id)

    if request.method == 'POST':
        legislacao.delete()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form-excluir.html', {'legislacao': legislacao})

def listar_protocolos(request):
    protocolos = ProtocoloEmpresa.objects.all()
    return render(request, 'empresas/listar_protocolos.html', {'protocolos': protocolos})

def novo_protocolo(request):
    if request.method == "POST":
        form = ProtocoloEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_protocolos')
    else:
        form = ProtocoloEmpresaForm()
    titulo = "Cadastrar protocolo"
    botao = "Cadastrar"
    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_protocolo(request, id):
    protocolo = get_object_or_404(ProtocoloEmpresa, id=id)
    if request.method == "POST":
        form = ProtocoloEmpresaForm(request.POST, instance=protocolo)
        if form.is_valid():
            form.save()
            return redirect('listar_protocolos')
    else:
        form = ProtocoloEmpresaForm(instance=protocolo)
    return render(request, 'empresas/form.html', {'form': form})

def excluir_protocolo(request, id):
    protocolo = get_object_or_404(ProtocoloEmpresa, id=id)
    if request.method == "POST":
        protocolo.delete()
        return redirect('listar_protocolos')
    return render(request, 'empresas/form-excluir.html', {'protocolo': protocolo})

def listar_inspecao(request):
    inspecoes = Inspecao.objects.all()
    return render(request, 'empresas/listar_inspecao.html', {'inspecoes': inspecoes})

def cadastrar_inspecao(request):
    titulo = "Cadastro de Inspeção"
    botao = "Cadastrar"
    if request.method == "POST":
        form = InspecaoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('listar_inspecao')
    else:
        form = InspecaoForm()
    return render(request, 'empresas/form-upload.html', {'form': form, 'titulo':titulo, 'botao':botao})


def alterar_inspecao(request, id):
    titulo = "Alterar Inspeção"
    botao = "Gravar"
    inspecao = Inspecao.objects.get(id=id)
    if request.method == "POST":
        form = InspecaoForm(request.POST, request.FILES, instance=inspecao)  # Adicionado request.FILES
        if form.is_valid():
            form.save()
            return redirect('listar_inspecao')
    else:
        form = InspecaoForm(instance=inspecao)
    return render(request, 'empresas/form.html', {'form': form, 'titulo':titulo, 'botao':botao})


def excluir_inspecao(request, id):
    inspecao = Inspecao.objects.get(id=id)
    if request.method == "POST":
        inspecao.delete()
        return redirect('listar_inspecao')
    return render(request, 'empresas/form-excluir.html', {'obj': inspecao})

def listar_acao_produtividade(request):
    acoes = AcaoProdutividade.objects.all()
    return render(request, 'empresas/listar_acao_produtividade.html', {'acoes': acoes})

def criar_acao_produtividade(request):
    if request.method == "POST":
        form = AcaoProdutividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_acao_produtividade')
    else:
        form = AcaoProdutividadeForm()
    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Criar Ação de Produtividade', 'botao': 'Salvar'})

def editar_acao_produtividade(request, id):
    acao = get_object_or_404(AcaoProdutividade, id=id)
    if request.method == "POST":
        form = AcaoProdutividadeForm(request.POST, instance=acao)
        if form.is_valid():
            form.save()
            return redirect('listar_acao_produtividade')
    else:
        form = AcaoProdutividadeForm(instance=acao)
    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Editar Ação de Produtividade', 'botao': 'Atualizar'})

def excluir_acao_produtividade(request, id):
    acao = get_object_or_404(AcaoProdutividade, id=id)
    if request.method == "POST":
        acao.delete()
        return redirect('listar_acao_produtividade')
    return render(request, 'empresas/form-excluir.html', {'obj': acao})






def listar_produtividade(request):
    produtividades = Produtividade.objects.all()
    return render(request, 'empresas/listar_produtividade.html', {'produtividades': produtividades})

def criar_produtividade(request, protocolo_id):
    acoes = AcaoProdutividade.objects.all()
    protocolo = ProtocoloEmpresa.objects.get(id=protocolo_id)

    if request.method == "POST":
        form = ProdutividadeForm(request.POST, initial={'protocolo': protocolo, 'fiscal_responsavel': protocolo.fiscal_responsavel})


        fiscais_auxiliares_ids = request.POST.getlist('fiscal_auxiliar')
        acoes_ids = request.POST.getlist('acoes')
        multiplicadores = request.POST.getlist('multiplicadores')

        if form.is_valid():
            produtividade = form.save(commit=False)
            produtividade.protocolo = protocolo
            produtividade.fiscal_responsavel = protocolo.fiscal_responsavel
            produtividade.save()
            produtividade.fiscal_auxiliar.set(fiscais_auxiliares_ids)

            for acao_id, multiplicador in zip(acoes_ids, multiplicadores):
                AcaoProdutividadeRel.objects.create(
                    acao_id=acao_id,
                    produtividade=produtividade,
                    multiplicador=multiplicador
                )

            produtividade.total = sum([
                rel.acao.pontos * rel.multiplicador
                for rel in produtividade.acaoprodutividaderel_set.all()
            ])
            produtividade.save()

            return redirect('listar_produtividade')
    else:
        form = ProdutividadeForm(initial={'protocolo': protocolo, 'fiscal_responsavel': protocolo.fiscal_responsavel})

    return render(request, 'empresas/form-produtividade.html', {
        'form': form, 
        'acoes': acoes, 
        'titulo': 'Criar Produtividade', 
        'botao': 'Salvar'
        
    })

"""Resolveu sim; Agora que o campo total  seja dinâmico usando ajax por exemplo para mostrar a prévia de quantos pontos serão enviados para o banco de dados, visto que ao selecionar o checkbox referente a cada acao, este já terá um valor de pontos associados, assim como quando digito um total no input do multiplicador relacionado a acao da produtividade:

"""

def editar_produtividade(request, id):
    produtividade = get_object_or_404(Produtividade, id=id)

    if request.method == 'POST':
        form = ProdutividadeFormEdit(request.POST, instance=produtividade, protocolo=produtividade.protocolo, fiscal_responsavel=produtividade.fiscal_responsavel)
        if form.is_valid():
            form.save()
            return redirect('listar_produtividade')
    else:
        form = ProdutividadeFormEdit(instance=produtividade, protocolo=produtividade.protocolo, fiscal_responsavel=produtividade.fiscal_responsavel)

    context = {
        'form': form,
        'produtividade': produtividade,
        # outros contextos necessários
    }

    return render(request, 'empresas/form-produtividade-editar.html', context)


def excluir_produtividade(request, id):
    produtividade = get_object_or_404(Produtividade, id=id)
    if request.method == "POST":
        produtividade.delete()
        return redirect('listar_produtividade')
    return render(request, 'empresas/form-excluir.html', {'obj': produtividade})


