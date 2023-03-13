from django.forms import forms
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,  BaseDetailView
from django.views.generic.list import ListView


from .models import Estado, Cidade, Bairro, Logradouro, Proprietario, Terreno, Protocolo, Infracao, Inspecao, Fiscal, Defesa #Reinspecao #Produtividade

#Método para redirecionar o usuário após ele efetuar um cadastro
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin #Importa views que protege o acesso de usuário não autenticado
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

#Primeiro criei uma view que é uma herança de CreateView
#Utilizo o nome da classe junto com a função para facilitar
#Ela tem três atributos: Modelo (classe), Fields (campos), Template_name
# e sucess_url (redirecionamento)

########################### CREATE ###########################
#class ProdutividadeCreate(LoginRequiredMixin, CreateView):
    #login_url = reverse_lazy('login')
   ## model = Produtividade
    #fields = ['descricao', 'pdf_teste']
   # template_name = 'form-upload.html'
  #  success_url = reverse_lazy('listar-produtividades')

   # def get_context_data(self, *args, **kwargs):
      #  context = super().get_context_data(*args, **kwargs)

        #Para personalizar a aparência para o usuário
      #  context['titulo'] = "Cadastro de produtividade"
     #   context['botao'] = "Cadastrar"

      #  return context

   # def form_valid(self, form):
   #     #Vou pegar os dados dos usuário no formulário
    #    form.instance.usuario = self.request.user #Está pegando o usuário que está logado
        #Antes do super a Protudividade não foi criada
    #    url = super().form_valid(form)
        #Depois do super a Produtividade foi criada
        #Quando chega neste ponto ele salvou no banco de dados da produtividade

        #self.object.descricao += " [TESTE]"
        #self.object.save()

        #Posso pegar qualquer atributo e mudar ainda
    #    return url

def get_queryset(self):
    txt_nome = self.request.GET.get('nome')

    if txt_nome:
        terrenos = Terreno.objects.filter(inscricao__icontains=txt_nome)
    else:
        terrenos = Terreno.objects.all()

    return terrenos

class ProtocoloDetalhes(DetailView):
    model = Protocolo
    template_name = 'detalhes-protocolo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        protocolo = self.object

        inspecoes = Inspecao.objects.filter(protocolo=protocolo).order_by('-data_inspecao1')
        infracoes = Infracao.objects.filter(inspecao__protocolo=protocolo).order_by('-id')

        context['inspecoes'] = inspecoes
        context['infracoes'] = infracoes

        return context



class EstadoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Estado
    fields = ['nome_estado', 'sigla_estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-estados')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de estado"
        context['botao'] = "Cadastrar"
        return context

class CidadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Cidade
    fields = ['nome_cidade', 'estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-cidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de cidade"
        context['botao'] = "Cadastrar"
        return context

class BairroCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Bairro
    fields = ['nome_bairro', 'cidade']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-bairros')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de bairro"
        context['botao'] = "Cadastrar"
        return context

class LogradouroCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Logradouro
    fields = ['tipo','nome_logradouro', 'bairro', 'cep']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-logradouros')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastros de logradouro"
        context['botao'] = "Cadastrar"
        return context

class ProprietarioCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Proprietario
    fields = ['nome_proprietario', 'logradouro_proprietario', 'numero_proprietario', 'complemento_proprietario']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-proprietarios')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de proprietário"
        context['botao'] = "Cadastrar"
        return context

class TerrenoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Terreno
    fields = ['inscricao', 'logradouro_terreno','numero_terreno','complemento_terreno',
              'proprietario','quadra', 'lote','area','logradouro_correspondencia',
              'numero_correspondencia','complemento_correspondencia','tipo_de_imovel']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-terrenos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de terreno"
        context['botao'] = "Cadastrar"
        return context

class ProtocoloCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Protocolo
    fields = ['protocolo','solicitante_protocolo','logradouro','descricao_protocolo','ouvidoria','status_protocolo','entrada_protocolo']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-protocolos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de protocolo"
        context['botao'] = "Cadastrar"
        return context

class FiscalCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Fiscal
    fields = ['nome_fiscal','matricula_fiscal','nivel','primeiro_nome']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-fiscais')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de fiscal"
        context['botao'] = "Cadastrar"
        return context

class InspecaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Inspecao
    fields = ['protocolo','terreno','foto_inspecao_1', 'data_inspecao1','horario_inspecao1','data_relatorio1','fiscal','produtidade_inspecao','limpo', 'mato','entulho', 'lixo', 'carcaca','material','pneu','outro','movel']
    template_name = 'form-upload.html'
    success_url = reverse_lazy('listar-inspecoes')
    ordering = ['terreno']
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de inspeção"
        context['botao'] = "Cadastrar"
        return context

class InfracaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['inspecao','data_auto', 'produtividade_infracao']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de infração"
        context['botao'] = "Cadastrar"
        return context

class DefesaCreate (LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Defesa
    fields = ['infracao', 'protocolo','entrada_protocolo','quem', 
              'grau', 'prazo_manifesto','email']
    template_name = 'form.html'
    success_url = reverse_lazy('gerenciar-infracoes')
    ordering = ['infracao']
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de defesas"
        context['botao'] = "Cadastrar"
        return context


#class ReinspecaoCreate (LoginRequiredMixin, CreateView):
 #  login_url = reverse_lazy('login')
 #  model = Reinspecao
 #   fields = ['defesa', 'data_inspecao2','horario_inspecao2','foto_inspecao_2','data_manifesto','produtividade_manifesto','situacao']
 #   template_name = 'form-upload2.html'
 #   success_url = reverse_lazy('listar-reinspecoes')
 #   ordering = ['defesa']
  #  def get_context_data(self, *args, **kwargs):
  #      context = super().get_context_data(*args, **kwargs)
#
  #      context['titulo'] = "Cadastro de Reinspeção"
 #       context['botao'] = "Cadastrar"
  #      return context

########################### UPDATE ###########################
#class ProdutividadeUpdate(LoginRequiredMixin, UpdateView):
   # login_url = reverse_lazy('login')
  #  model = Produtividade
 #   fields = ['descricao', 'pdf_teste']
  #  template_name = 'form-upload.html'
 #   success_url = reverse_lazy('listar-produtividade')

  #  def get_context_data(self, *args, **kwargs):
  #      context = super().get_context_data(*args, **kwargs)

    #    #Para personalizar a aparência para o usuário
   #     context['titulo'] = "Editar cadastro de produtividade"
    #    context['botao'] = "Salvar"

     #   return context

  #  def get_object(self, queryset=None):
   #     self.object = get_object_or_404(Produtividade, pk=self.kwargs['pk'], usuario=self.request.user)
   #     return self.object


class EstadoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Estado
    fields = ['nome_estado', 'sigla_estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-estados')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de estado"
        context["botao"] = "Gravar"

        return context

class CidadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Cidade
    fields = ['nome_cidade', 'estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-cidades')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de cidade"
        context["botao"] = "Gravar"

        return context

class BairroUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Bairro
    fields = ['nome_bairro', 'cidade']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-bairros')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de bairro"
        context["botao"] = "Gravar"

        return context

class LogradouroUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Logradouro
    fields = ['tipo','nome_logradouro', 'bairro', 'cep']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-logradouros')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de logradouro"
        context["botao"] = "Gravar"
        return context

class ProprietarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Proprietario
    fields = ['nome_proprietario', 'logradouro_proprietario', 'numero_proprietario', 'complemento_proprietario']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-proprietarios')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de proprietário"
        context["botao"] = "Gravar"

        return context

class TerrenoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Terreno
    fields = ['inscricao', 'logradouro_terreno','numero_terreno','complemento_terreno',
              'proprietario', 'lote','quadra','area','logradouro_correspondencia',
              'numero_correspondencia','complemento_correspondencia', 'tipo_de_imovel']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-terrenos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de terreno"
        context["botao"] = "Gravar"

        return context

class ProtocoloUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Protocolo
    fields = ['protocolo', 'solicitante_protocolo', 'logradouro', 'descricao_protocolo', 'ouvidoria', 'observacoes',
              'status_protocolo', 'entrada_protocolo', 'encerramento_protocolo']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-protocolos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de protocolo"
        context["botao"] = "Gravar"
        return context

class FiscalUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Fiscal
    fields = ['nome_fiscal','matricula_fiscal','nivel','primeiro_nome']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-fiscais')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de fiscal"
        context["botao"] = "Gravar"
        return context

class InspecaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Inspecao
    fields = ['protocolo','terreno','foto_inspecao_1','data_inspecao1','horario_inspecao1','data_relatorio1','fiscal','produtidade_inspecao','limpo', 'mato','entulho', 'lixo', 'carcaca','material','pneu','outro','movel']
    template_name = 'form-upload.html'
    success_url = reverse_lazy('listar-inspecoes')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição da inspeção"
        context["botao"] = "Gravar"
        return context

class InfracaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['inspecao', 'data_auto','rastreio_infracao','status_rastreio','data_entrega_autuacao','prazo_defesa','nome_recebedor','numero_format_ano','protocolo_defesa','entrada_protocolo','quem','prazo_manifesto','foto_inspecao_2','data_inspecao2','horario_inspecao2','data_manifesto','julgamento','situacao','rastreio_julgamento','status_rastreio_julgamento','data_entrega_julgamento','produtividade_infracao','produtividade_manifesto', 'email']
    template_name = 'form-upload2.html'
    success_url = reverse_lazy('gerenciar-infracoes')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de infração"
        context["botao"] = "Gravar"
        return context

class ARCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano','rastreio_infracao','status_rastreio','data_entrega_autuacao','nome_recebedor', 'prazo_defesa']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Controle de AR's"
        context["botao"] = "Gravar"
        return context

class DefesasCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano','protocolo_defesa','entrada_protocolo','quem', 'prazo_manifesto','email']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Controle de defesas"
        context["botao"] = "Gravar"
        return context

class ReinspecoesCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano','foto_inspecao_2','data_inspecao2','horario_inspecao2','data_manifesto','produtividade_manifesto','situacao','julgamento']
    template_name = 'form-upload2.html'
    success_url = reverse_lazy('listar-infracoes')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if form.instance.status_rastreio != 'ENTREGUE':
            form.fields['situacao'].choices = (
                ("", "---------"),
                ("6", "Não recebeu e limpou"),
                ("4", "Manifesto e julgamento fora do sistema"),
                ("7", "Edital"),
                ("9", "Não defendeu e limpou via Edital"),
                ("10", "Perda de prazo")
            )
        elif form.instance.status_rastreio == 'ENTREGUE' and not form.instance.protocolo_defesa:
            form.fields['situacao'].choices = (
                ("", "---------"),
                ("2", "Não defendeu e limpou"),
                ("13", "Não defendeu e limpou meia boca"),
                ("3", "Não defendeu e não limpou"),
                ("4", "Manifesto e julgamento fora do sistema"),
                ("8", "Não defendeu e não limpou via Edital"),
                ("9", "Não defendeu e limpou via Edital"),
                ("10", "Perda de prazo"),
                ("11", "Erro na identificação"),
                ("12", "Mudança do proprietário no decorrer do processo")
            )
        else:
            form.fields['situacao'].choices = (
                ("", "---------"),
                ("1", "Defendeu e limpou"),
                ("4", "Manifesto e julgamento fora do sistema"),
                ("5", "Defendeu após o prazo e limpou"),
                ("10", "Perda de prazo"),
                ("11", "Erro na identificação"),
                ("12", "Mudança do proprietário no decorrer do processo")
            )
        return form



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastrar reinspeção"
        context["botao"] = "Gravar"
        return context

class ARJulgamento(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano','rastreio_julgamento','status_rastreio_julgamento','data_entrega_julgamento']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Controle de AR's julgamento"
        context["botao"] = "Gravar"
        return context



class DefesaUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Defesa
    fields = ['infracao','protocolo','entrada_protocolo','quem', 'grau', 'prazo_manifesto']
    template_name = 'form.html'
    success_url = reverse_lazy('gerenciar-infracoes')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de defesas"
        context['botao'] = "Atualizar"
        return context

#class ReinspecaoUpdate(LoginRequiredMixin, UpdateView):
   # login_url = reverse_lazy('login')
  #  model = Reinspecao
   # fields = ['defesa', 'data_inspecao2','horario_inspecao2','foto_inspecao_2','data_manifesto','situacao']
   # template_name = 'form-upload.html'
   # success_url = reverse_lazy('listar-reinspecoes')
  #  def get_context_data(self, *args, **kwargs):
   #     context = super().get_context_data(*args, **kwargs)
#
   #     context['titulo'] = "Edição de reinspeção"
   #     context['botao'] = "Atualizar"
   #     return context





########################### DELETE ###########################
#class ProdutividadeDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
   # group_required = u"Administrador"
   # login_url = reverse_lazy('login')
  #  model = Produtividade
  #  template_name = 'form-excluir.html'
  #  success_url = reverse_lazy('listar-produtividades')

    #def get_object(self, queryset=None):
     #   self.object = get_object_or_404(Produtividade, pk=self.kwargs['pk'], usuario=self.request.user)
     #   return self.object


class EstadoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Administrador"
    login_url = reverse_lazy('login')
    model = Estado
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-estados')

class CidadeDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Cidade
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-cidades')

class BairroDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Bairro
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-bairros')

class LogradouroDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Logradouro
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-logradouros')

class ProprietarioDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Proprietario
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-proprietarios')

class TerrenoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Terreno
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-terrenos')

class ProtocoloDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Protocolo
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-protocolos')

class FiscalDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Fiscal
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-fiscais')

class InspecaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-inspecoes')

class InfracaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-infracoes-ativos')

class DefesaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Defesa
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('gerenciar-infracoes')
    
#class ReinspecaoDelete(LoginRequiredMixin, DeleteView):
  #  login_url = reverse_lazy('login')
  #  model = Reinspecao
  #  template_name = 'form-excluir.html'
  #  success_url = reverse_lazy('listar-reinspecoes')
 



########################### LISTA ###########################

class EstadoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Estado
    template_name = 'listar-estados.html'

class CidadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Cidade
    template_name = 'listar-cidades.html'

class BairroList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Bairro
    template_name = 'listar-bairros.html'

class LogradouroList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Logradouro
    template_name = 'listar-logradouros.html'

class ProprietarioList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Proprietario
    template_name = 'listar-proprietarios.html'

class TerrenoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Terreno
    template_name = 'listar-terrenos.html'

class ProtocoloList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Protocolo
    template_name = 'listar-protocolos.html'

class FiscalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Fiscal
    template_name = 'listar-fiscais.html'
    ordering = ['nome_fiscal']

class InspecaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'listar-inspecoes.html'

class InfracaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes.html'

class InfracaoListFilterAtivos(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes-ativos.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(julgamento__isnull=True)
        return queryset

class ProdutividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'listar-produtividades.html'
    ordering = ['data_inspecao1']

class ProdutividadeList2(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-produtividades2.html' 


class ProdutividadeList3(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-produtividades3.html'


class InfracaoList2(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Defesa
    template_name = 'gerenciar-defesas.html'

class GerenciarList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'gerenciar-infracoes.html'

class InformacoesList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes2.html'

#class ReinspecaoList(LoginRequiredMixin, ListView):
   # login_url = reverse_lazy('login')
  #  model = Reinspecao
  #  template_name = 'listar-reinspecoes.html'


def gerar_relatorio(request,pk,template_name="gerar_relatorio.html"):
    inspecao = get_object_or_404(Inspecao, pk=pk)
    return render(request, template_name, {'inspecao':inspecao})

def gerar_manifestacao(request,pk,template_name="gerar_manifestacao.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_julgamento(request,pk,template_name="gerar_julgamento.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar1(request,pk,template_name="gerar_ar1.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar2(request,pk,template_name="gerar_ar2.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar3(request,pk,template_name="gerar_ar3.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar4(request,pk,template_name="gerar_ar4.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar5(request,pk,template_name="gerar_ar5.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_ar6(request,pk,template_name="gerar_ar6.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})
    
def gerar_ar7(request,pk,template_name="gerar_ar7.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

def gerar_auto(request,pk,template_name="auto_infracao.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao':infracao})

