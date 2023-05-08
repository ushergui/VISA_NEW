from django.shortcuts import render, redirect
from .models import Contabilidade, Cnae, Empresas
from .forms import ContabilidadeForm, CnaeForm, EmpresasForm, RiscoForm

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

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form})

def editar_cnae(request, id):
    cnae = Cnae.objects.get(id=id)
    form = CnaeForm(request.POST or None, instance=cnae)

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form})

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

    if form.is_valid():
        empresa = form.save(commit=False)
        # Aqui você pode adicionar a lógica para definir o risco da empresa com base nos CNAEs selecionados
        empresa.save()
        form.save_m2m()
        return redirect('listar_empresas')

    return render(request, 'empresas/form.html', {'form': form})

def editar_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    form = EmpresasForm(request.POST or None, instance=empresa)

    if form.is_valid():
        empresa = form.save(commit=False)
        # Aqui você pode adicionar a lógica para redefinir o risco da empresa com base nos CNAEs selecionados
        empresa.save()
        form.save_m2m()
        return redirect('listar_empresas')

    return render(request, 'empresas/form.html', {'form': form})

def excluir_empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if request.method == 'POST':
        empresa.delete()
        return redirect('listar_empresas')

    return render(request, 'empresas/confirmar_exclusao.html', {'obj': empresa})

def listar_risco(request):
    riscos = Risco.objects.all()
    return render(request, 'empresas/listar_risco.html', {'riscos': riscos})

def cadastrar_risco(request):
    form = RiscoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form})

def editar_risco(request, id):
    risco = get_object_or_404(Risco, id=id)
    form = RiscoForm(request.POST or None, instance=risco)

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form})

def excluir_risco(request, id):
    risco = get_object_or_404(Risco, id=id)

    if request.method == 'POST':
        risco.delete()
        return redirect('listar_risco')

    return render(request, 'empresas/form-excluir.html', {'risco': risco})

