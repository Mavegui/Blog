from . import views
from django.urls import path


urlpatterns = [
    # Index
    path('',  views.index, name='index'),
    
    
    # ================
    # CATEGORIAS
    # ================
    path('categorias/', views.categorias, name='categorias'),
    
    # Categoria visualizar por slug
    path(
        'categorias/<categoria_slug>/',
        views.categoria,
        name='categoria'
    ),
    
    # Nova categoria
    path(
        'nova_categoria/',
        views.nova_categoria,
        name='nova_categoria'
    ),
    
    # Editar categoria
    path(
        'edit_categoria/<categoria_id>/',
        views.edit_categoria,
        name='edit_categoria'
    ),
    
    # Deletar categoria
    path(
        'delete_categoria/<categoria_id>/',
        views.delete_categoria,
        name='delete_categoria'
    ),
    
    
    # ================
    # POSTAGENS
    # ================
    path('postagens/', views.postagens, name='postagens'),
    
    # Postagem visualizar por slug
    path(
        'postagens/<postagem_slug>/',
        views.postagem,
        name='postagem'
    ),
    
    # Nova postagem
    path(
        'nova_postagem/<categoria_id>/',
        views.nova_postagem,
        name='nova_postagem'
    ),
    
    # Editar postagem
    path(
        'edit_postagem/<postagem_id>/',
        views.edit_postagem,
        name='edit_postagem'
    ),
    
    # Deletar postagem
    path(
        'delete_postagem/<postagem_id>/',
        views.delete_postagem,
        name='delete_postagem'
    ),
    
]

    