from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'
    ),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    
    path('perfil', views.perfil, name='perfil'),
    
    path('edit_perfil', views.edit_perfil, name='edit_perfil'),
    path('delete_conta', views.delete_conta, name='delete_conta'),
    
    path('alterar_senha', views.alterar_senha, name='alterar_senha'),
    
]