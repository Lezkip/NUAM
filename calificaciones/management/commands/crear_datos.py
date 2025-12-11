"""Django management command to create fictitious data."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from calificaciones.models import Emisor, FactorTributario, Calificacion, HistorialAuditoria
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Crea datos ficticios para pruebas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('CREANDO DATOS FICTICIOS'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        try:
            usuarios = self.crear_usuarios()
            emisores = self.crear_emisores()
            factores = self.crear_factores()
            self.crear_calificaciones(emisores, factores, usuarios)
            self.crear_auditoria_manual(emisores, usuarios)
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('✓ DATOS FICTICIOS CREADOS EXITOSAMENTE'))
            self.stdout.write(self.style.SUCCESS('='*60))
            self.stdout.write(self.style.WARNING('\nCredenciales de prueba:'))
            self.stdout.write('  Admin: admin / admin123')
            self.stdout.write('  Analista: analista / analista123')
            self.stdout.write('  Corredor: corredor / corredor123')
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            import traceback
            traceback.print_exc()

    def crear_usuarios(self):
        """Crear usuarios de prueba"""
        usuarios = []
        
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            usuarios.append(admin)
            self.stdout.write(self.style.SUCCESS('✓ Usuario Admin creado'))
        else:
            usuarios.append(User.objects.get(username='admin'))
        
        # Analista (is_staff=True)
        if not User.objects.filter(username='analista').exists():
            analista = User.objects.create_user('analista', 'analista@example.com', 'analista123')
            analista.is_staff = True
            analista.save()
            usuarios.append(analista)
            self.stdout.write(self.style.SUCCESS('✓ Usuario Analista creado'))
        else:
            usuarios.append(User.objects.get(username='analista'))
        
        # Corredor (usuario normal)
        if not User.objects.filter(username='corredor').exists():
            corredor = User.objects.create_user('corredor', 'corredor@example.com', 'corredor123')
            usuarios.append(corredor)
            self.stdout.write(self.style.SUCCESS('✓ Usuario Corredor creado'))
        else:
            usuarios.append(User.objects.get(username='corredor'))
        
        return usuarios

    def crear_emisores(self):
        """Crear emisores ficticios"""
        emisores_data = [
            {'rut': '76.123.456-7', 'nombre': 'Empresa XYZ S.A.', 'direccion': 'Av. Principal 123, Santiago'},
            {'rut': '77.234.567-8', 'nombre': 'Comercial ABC Ltda.', 'direccion': 'Calle Central 456, Valparaíso'},
            {'rut': '78.345.678-9', 'nombre': 'Industria DEF SpA', 'direccion': 'Camino Sur 789, Concepción'},
            {'rut': '79.456.789-0', 'nombre': 'Servicios GHI E.I.R.L.', 'direccion': 'Pasaje Oriente 321, Temuco'},
            {'rut': '80.567.890-1', 'nombre': 'Constructora JKL S.A.', 'direccion': 'Av. Libertad 654, Puerto Montt'},
        ]
        
        emisores = []
        for data in emisores_data:
            emisor, created = Emisor.objects.get_or_create(
                rut=data['rut'],
                defaults={
                    'nombre': data['nombre'],
                    'direccion': data['direccion'],
                    'activo': True,
                    'fecha_registro': datetime.now()
                }
            )
            if created:
                self.stdout.write(f'✓ Emisor creado: {data["nombre"]}')
            emisores.append(emisor)
        
        return emisores

    def crear_factores(self):
        """Crear factores tributarios ficticios"""
        factores_data = [
            {'codigo': 'FT-001', 'descripcion': 'Factor de Riesgo Fiscal Bajo'},
            {'codigo': 'FT-002', 'descripcion': 'Factor de Riesgo Fiscal Medio'},
            {'codigo': 'FT-003', 'descripcion': 'Factor de Riesgo Fiscal Alto'},
            {'codigo': 'FT-004', 'descripcion': 'Factor de Cumplimiento Tributario'},
            {'codigo': 'FT-005', 'descripcion': 'Factor de Historial Comercial'},
        ]
        
        factores = []
        for data in factores_data:
            factor, created = FactorTributario.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'descripcion': data['descripcion'],
                    'vigente': True
                }
            )
            if created:
                self.stdout.write(f'✓ Factor creado: {data["codigo"]}')
            factores.append(factor)
        
        return factores

    def crear_calificaciones(self, emisores, factores, usuarios):
        """Crear calificaciones ficticias"""
        admin = usuarios[0] if usuarios else None
        
        if not admin:
            self.stdout.write(self.style.ERROR('✗ No hay usuarios para crear calificaciones'))
            return
        
        # Crear 15 calificaciones aleatorias
        count = 0
        for _ in range(15):
            emisor = random.choice(emisores)
            factor = random.choice(factores)
            
            # Evitar duplicados (unique_together)
            if Calificacion.objects.filter(emisor=emisor, factor=factor).exists():
                continue
            
            fecha_pasada = datetime.now() - timedelta(days=random.randint(1, 90))
            
            calificacion = Calificacion.objects.create(
                emisor=emisor,
                factor=factor,
                usuario=admin,
                fecha_asignacion=fecha_pasada,
                comentario=random.choice([
                    'Calificación regular',
                    'Requiere seguimiento',
                    'Excelente cumplimiento',
                    'Pendiente actualización',
                    'Riesgo moderado'
                ])
            )
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {count} Calificaciones creadas'))

    def crear_auditoria_manual(self, emisores, usuarios):
        """Crear registros manuales de auditoría"""
        admin = usuarios[0] if usuarios else None
        
        if not admin:
            self.stdout.write(self.style.ERROR('✗ No hay usuarios para crear auditoría'))
            return
        
        count = 0
        for emisor in emisores[:3]:  # Auditoría para los primeros 3 emisores
            # Crear 2-3 registros de cambio por emisor
            for i in range(random.randint(2, 3)):
                fecha_pasada = datetime.now() - timedelta(days=random.randint(1, 60))
                
                auditoria = HistorialAuditoria.objects.create(
                    usuario=admin,
                    emisor=emisor,
                    factor_anterior=f'FT-{random.randint(1,5):03d}',
                    factor_nuevo=f'FT-{random.randint(1,5):03d}',
                    fecha=fecha_pasada
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {count} Registros de Auditoría creados'))
