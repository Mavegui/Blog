from django import forms
from .models import Categoria, Postagem, Comentario

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        labels = {
            'nome': 'Nome',
        }
    
class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'descricao', 'conteudo', 'categoria']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'conteudo': 'Conteúdo',
            'categoria': 'Categoria',
        }
        widgets = {
            'conteudo': forms.Textarea(attrs={'cols': 80}),
        }
        
class ComentarioForm(forms.ModelForm):
    """
    Formulário para adicionar um comentário
    
        - Valida o campo de comentário
        - Evita erros como exibir none no campo. 
    """
    class Meta:
        model = Comentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu comentário...',
                'rows': 3
            })
        }
