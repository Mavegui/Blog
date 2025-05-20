
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Postagem, Categoria, Comentario
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PostagemForm, CategoriaForm, ComentarioForm


# Index
def index(request):
    return render(request, 'blogs/index.html')


# =======================
# CATEGORIAS PARTE
# =======================
def categorias(request):
    """Mostra todas as categorias"""
    categoria = Categoria.objects.all().order_by('data_adicionada')
    context = {'categorias': categoria}
    return render(request, 'blogs/categorias/categorias.html', context)


def categoria(request, categoria_slug):
    """Mostra uma categoria por id"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    postagens = categoria.postagem_set.order_by('-data_adicionada')
    context = {'categoria': categoria, 'postagens': postagens}
    
    return render(request, 'blogs/categorias/categoria.html', context)


@login_required
def nova_categoria(request):
    """
    Adiciona uma nova categoria
    
        - Somente superusuário pode realizar a ação
    """
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('categorias')
        )
    
    if request.method != 'POST':
        form = CategoriaForm()
    else:
        form = CategoriaForm(data=request.POST)
        if form.is_valid():
            nova_categoria = form.save(commit=False)
            nova_categoria.owner = request.user
            nova_categoria.save()
            return HttpResponseRedirect(reverse('categorias'))
        else:
            print(form.errors)
    
    context = {'form': form}
    return render(request, 'blogs/categorias/nova_categoria.html', context)


@login_required
def edit_categoria(request, categoria_id):
    """
    Edita uma categoria
    
        - Somente superusuário pode realizar a ação
    """
    categoria = Categoria.objects.get(id=categoria_id)
    
    if categoria.owner != request.user:
        raise Http404
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('categorias')
        )
    
    if request.method != 'POST':
        # Preenche o formulário com a categoria atual
        form = CategoriaForm(instance=categoria)
    else:
        # Processa o formulário
        form = CategoriaForm(instance=categoria, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('categorias')
            )
            
    context = {'form': form, 'categoria': categoria}
    return render(request, 'blogs/categorias/edit_categoria.html', context)


@login_required
def delete_categoria(request, categoria_id):
    """
    Deleta uma categoria
    
        - Somente superusuário pode realizar a ação
    """
    categoria = Categoria.objects.get(id=categoria_id)
    
    if categoria.owner != request.user:
        raise Http404
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('categorias')
        )
    
    if request.method == 'POST':
        categoria.delete()
        return HttpResponseRedirect(
            reverse(
                'categorias'
            )
        )
    
    context = {'categoria': categoria}
    return render(request, 'blogs/categorias/delete_categoria.html', context)


# =======================
# POSTAGENS PARTE
# =======================
def postagens(request):
    """Mostra todas as postagens"""
    postagens = Postagem.objects.all().order_by('data_adicionada')
    categoria = Categoria.objects.first()
    context = {'postagens': postagens, 'categoria': categoria}
    return render(request, 'blogs/postagens/postagens.html', context)


def postagem(request, postagem_slug):
    """
    Exibe uma postagem específica
    
        - Exibição de dados da postagem
        - Exibição, edição e exclusão de comentários
        - Formulário para adicionar novos comentários
    """
    postagem = get_object_or_404(Postagem, slug=postagem_slug)

    edit_comentario = None
    comentario_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')

    # Lógica de deletar comentário
    if delete_id and request.user.is_authenticated:
        delete_comentario = get_object_or_404(
            Comentario,
            id=delete_id,
            postagem=postagem
        )
        
        if delete_comentario.owner == request.user:
            delete_comentario.delete()
        
            return redirect(
                reverse(
                    'postagem',
                    args=[postagem.slug]
                )
            )

    # Lógica de adicionar novo comentário e editar comentário existente
    if not comentario_id or not request.user.is_authenticated:
        # Adiciona novo comentário
        if request.method != 'POST':
            form = ComentarioForm()
        else:
            form = ComentarioForm(request.POST)
    
    else:
        # Edição de comentário existente
        edit_comentario = get_object_or_404(
            Comentario,
            id=comentario_id,
            postagem=postagem
        )
    
        if edit_comentario.owner != request.user:
            return redirect('postagem', postagem.slug)
    
        if request.method == 'POST':
            form = ComentarioForm(request.POST, instance=edit_comentario)
        else:
            form = ComentarioForm(instance=edit_comentario)
    
    if request.method == 'POST' and request.user.is_authenticated:
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.postagem = postagem
            novo_comentario.owner = request.user
            novo_comentario.data_adicionada = timezone.now()
            novo_comentario.save()
    
            return redirect(reverse('postagem', args=[postagem.slug]))
    
    context = {
        'postagem': postagem,
        'comentarios': postagem.comentarios.all().order_by('-data_adicionada'),
        'form': form,
        'comentario_id': int(comentario_id) if comentario_id else None
    }
    
    return render(request, 'blogs/postagens/postagem.html', context)
    

@login_required
def nova_postagem(request, categoria_id):
    """
    Adiciona uma nova postagem
    
        - Somente superusuário pode realizar a ação
    """
    categoria = Categoria.objects.get(id=categoria_id)
    if categoria.owner != request.user:
        raise Http404
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('postagens')
        )
    
    if request.method != 'POST':
        form = PostagemForm()
    else:
        form = PostagemForm(data=request.POST)
        if form.is_valid():
            nova_postagem = form.save(commit=False)
            nova_postagem.owner = request.user
            nova_postagem.save()
            return HttpResponseRedirect(
                reverse('postagens')
            )
        else:
            print(form.errors)
    
    context = {'categoria':categoria, 'form': form}
    return render(request, 'blogs/postagens/nova_postagem.html', context)


@login_required
def edit_postagem(request, postagem_id):
    """
    Edita uma postagem
    
        - Somente superusuário pode realizar a ação
    """
    postagem = Postagem.objects.get(id=postagem_id)
    
    if postagem.owner != request.user:
        raise Http404
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('postagens')
        )
    
    if request.method != 'POST':
        # Preenche o formulário com a postagem atual
        form = PostagemForm(instance=postagem)
    else:
        # Processa o formulário
        form = PostagemForm(instance=postagem, data=request.POST)
        if form.is_valid():
            postagem_editada = form.save(commit=False)
            postagem_editada.owner = request.user
            postagem_editada.slug = None
            postagem_editada.save()
            return HttpResponseRedirect(
                reverse(
                    'postagens'
                )
            )
        else:
            print("Formulário inválido:", form.errors)

    context = {'form': form, 'postagem': postagem}
    return render(request, 'blogs/postagens/edit_postagem.html', context)


@login_required
def delete_postagem(request, postagem_id):
    """
    Deleta uma postagem
    
        - Somente superusuário pode realizar a ação
    """
    postagem = Postagem.objects.get(id=postagem_id)
    categoria = postagem.categoria
    
    if postagem.owner != request.user:
        raise Http404
    
    if not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('postagens')
        )
    
    if request.method == 'POST':
        postagem.delete()
        return HttpResponseRedirect(
            reverse(
                'postagens'
            )
        )
    
    context = {'postagem': postagem, 'categoria': categoria}
    return render(request, 'blogs/postagens/delete_postagem.html', context)
