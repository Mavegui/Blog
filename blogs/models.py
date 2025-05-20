from django.db import models
from django.utils.text import slugify

"""
Página responsável pela estruturação do banco de dados.
    
Preciso rodar os seguintes comandos:
    - python3 manage.py makemigrations
    - python3 manage.py migrate

"""

class Categoria(models.Model):
    """
    Classe que representa categoria de postagens.
    """
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    data_adicionada = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
class Postagem(models.Model):
    """
    Classe que representa uma postagem.
        
        - Slug de postagem é a junção de slug gerado do título e o slug da categoria.
        - O slug é gerado automaticamente quando a postagem é criada.
        - Slug únicos, se existir atribui númeração no fim do slug.
    """
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_adicionada = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    
    slug = models.SlugField(blank=True, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.titulo}-{self.categoria.slug}")
            original_slug = self.slug
            counter = 1
            while Postagem.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
            super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Postagens'
 
    def __str__(self):
        return self.titulo[:50] + '...'
    
class Comentario(models.Model):
    """
    Classe que representa um comentário.
    """
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    data_adicionada = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.comentario[:50] + '...'