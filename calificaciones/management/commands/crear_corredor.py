from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea un usuario "corredor" con permisos de solo lectura (sin staff, no puede ver auditoría)'

    def handle(self, *args, **options):
        username = 'corredor'
        password = '1234'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario "{username}" ya existe.'))
            return
        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=False,  # Sin permisos de staff = no puede ver auditoría
            is_superuser=False,
            first_name='Corredor',
            last_name='Sistema'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Usuario "{username}" creado exitosamente con solo lectura (sin acceso a auditoría).'))
