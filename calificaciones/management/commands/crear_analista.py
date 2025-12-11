from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea un usuario "analista" con permisos de staff (puede editar y ver auditoría)'

    def handle(self, *args, **options):
        username = 'analista'
        password = '1234'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario "{username}" ya existe.'))
            return
        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=True,  # Permisos de staff = puede crear/editar/eliminar y ver auditoría
            is_superuser=False,
            first_name='Analista',
            last_name='Sistema'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Usuario "{username}" creado exitosamente con permisos de Analista (staff).'))
