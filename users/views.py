from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import EditPerfilForm

def logout_view(request):
    """
    Faz logout do usuário.
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    """
    Registra novo usuário.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticate_user = authenticate(
                username=new_user.username, 
                password=request.POST['password1']
            )
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def perfil(request):
    """
    Exibe o perfil do usuário logado.
        - O usuário visualiza seus dados
        - O usuário tem três links:
            - Editar perfil
            - Alterar senha 
            - Excluir conta  
    """
    if request.method != 'POST':
        form = UserChangeForm(instance=request.user)
    else:
        form = UserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('perfil'))
    
    context = {'form': form}
    return render(request, 'users/profile/perfil.html', context)


@login_required
def edit_perfil(request):
    """
    Edita o perfil do usuário logado.
        - O usuário pode editar
             - Usuário
             - Email
             - Nome
             - Sobrenome
    """
    if request.method != 'POST':
        form = EditPerfilForm(instance=request.user)
    else:
        form = EditPerfilForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('perfil'))
    
    context = {'form': form}
    return render(request, 'users/profile/edit_perfil.html', context)


@login_required
def alterar_senha(request):
    """
    Altera a senha do usuário logado.
        - O usuário pode alterar sua senha
    """
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('perfil'))
    
    context = {'form': form}
    return render(request, 'users/profile/alterar_senha.html', context)


@login_required
def delete_conta(request):
    """
    Exclui a conta do usuário logado.
        - O usuário pode excluir sua conta
    """
    if request.method == 'POST':
        request.user.delete()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'users/profile/delete_conta.html')

