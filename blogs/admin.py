from django.contrib import admin
from blogs.models import Categoria, Postagem

# Preciso sempre importar models aqui, para aparecer no Admin

admin.site.register(Categoria)
admin.site.register(Postagem)
