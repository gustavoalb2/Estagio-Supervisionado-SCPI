import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scpi.settings')
django.setup()

from django.contrib.auth.models import User
from scpiapp.models import Usuario

def criar_usuario_comum():
    # Verificar se o usuário já existe
    if User.objects.filter(username='propeg').exists():
        print('Usuário comum (propeg) já existe')
        return User.objects.get(username='propeg')
    
    # Criar usuário comum no sistema de autenticação do Django
    usuario_comum = User.objects.create_user(
        username='propeg',
        email='propeg@example.com',
        password='propeg',
        first_name='Usuário',
        last_name='Comum'
    )
    
    # Criar perfil correspondente no nosso modelo personalizado
    usuario_model = Usuario.objects.create(
        nome='Usuário Comum',
        email='propeg@example.com',
        tipo='comum'
    )
    
    print('Usuário comum (propeg) criado com sucesso')
    return usuario_comum

def criar_usuario_admin():
    # Verificar se o usuário já existe
    if User.objects.filter(username='admin').exists():
        print('Usuário admin já existe')
        return User.objects.get(username='admin')
    
    # Criar usuário admin no sistema de autenticação do Django
    usuario_admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin',
        first_name='Administrador',
        last_name='Sistema'
    )
    
    # Criar perfil correspondente no nosso modelo personalizado
    usuario_model = Usuario.objects.create(
        nome='Administrador Sistema',
        email='admin@example.com',
        tipo='admin'
    )
    
    print('Usuário admin criado com sucesso')
    return usuario_admin

if __name__ == '__main__':
    print("Criando usuários para o sistema SCPI...")
    criar_usuario_comum()
    criar_usuario_admin()
    print('Configuração de usuários concluída!')
    
    print("\nUsuários criados:")
    for user in User.objects.all():
        print(f"- {user.username} ({user.email})")