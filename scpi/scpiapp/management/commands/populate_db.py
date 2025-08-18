import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from scpiapp.models import Usuario, Processo, Notificacao, Relatorio, Auditoria
from faker import Faker

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write('Limpando dados antigos...')
        Auditoria.objects.all().delete()
        Relatorio.objects.all().delete()
        Notificacao.objects.all().delete()
        Processo.objects.all().delete()
        Usuario.objects.exclude(is_superuser=True).delete()

        fake = Faker('pt_BR')

        self.stdout.write('Criando usuários...')
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'tipo': Usuario.TiposUsuario.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Usuário admin criado.'))

        comum_user, created = Usuario.objects.get_or_create(
            username='comum',
            defaults={
                'email': 'comum@example.com',
                'first_name': 'Usuário',
                'last_name': 'Comum',
                'tipo': Usuario.TiposUsuario.COMUM,
            }
        )
        if created:
            comum_user.set_password('comum123')
            comum_user.save()
            self.stdout.write(self.style.SUCCESS('Usuário comum criado.'))

        usuarios = [admin_user, comum_user]
        for i in range(5):
            username = fake.user_name()
            user, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': fake.email(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'tipo': Usuario.TiposUsuario.COMUM,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            usuarios.append(user)

        self.stdout.write(self.style.SUCCESS(f'{len(usuarios)} usuários criados.'))

        self.stdout.write('Criando processos...')
        setores = ['Financeiro', 'RH', 'TI', 'Operações', 'Marketing']
        processos = []
        for i in range(20):
            data_abertura = fake.date_between(start_date='-1y', end_date='today')
            
            processo = Processo.objects.create(
                numero=f'PROC-{2025000 + i}',
                setor_origem=random.choice(setores),
                data_abertura=data_abertura,
                status=random.choice(Processo.StatusProcesso.choices)[0],
                descricao=fake.paragraph(nb_sentences=3),
                criado_por=random.choice(usuarios)
            )
            processos.append(processo)
        self.stdout.write(self.style.SUCCESS(f'{len(processos)} processos criados.'))

        self.stdout.write('Criando notificações...')
        for processo in processos:
            if random.random() > 0.5:
                Notificacao.objects.create(
                    processo=processo,
                    usuario=random.choice(usuarios),
                    mensagem=f'O status do processo {processo.numero} foi atualizado.',
                    lida=random.choice([True, False])
                )
        self.stdout.write(self.style.SUCCESS('Notificações criadas.'))
        
        self.stdout.write('Criando auditorias...')
        for processo in processos:
            for _ in range(random.randint(1, 3)):
                Auditoria.objects.create(
                    processo=processo,
                    usuario=random.choice(usuarios),
                    acao=random.choice(Auditoria.AcoesAuditoria.choices)[0],
                    detalhes=f'Detalhes da ação de auditoria para o processo {processo.numero}.'
                )
        self.stdout.write(self.style.SUCCESS('Registros de auditoria criados.'))


        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
