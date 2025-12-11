from django.core.management.base import BaseCommand
from calificaciones.models import Emisor, FactorTributario, Calificacion
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea emisores, factores y calificaciones ficticias'

    def handle(self, *args, **options):
        # Crear emisores ficticios
        emisores_data = [
            {'rut': '12.345.678-9', 'nombre': 'Empresa A SpA', 'direccion': 'Av. Principal 1000, Santiago'},
            {'rut': '23.456.789-0', 'nombre': 'Comercial B Ltda', 'direccion': 'Calle Central 500, Valparaíso'},
            {'rut': '34.567.890-1', 'nombre': 'Transportes C SA', 'direccion': 'Ruta 5 Norte, Concepción'},
            {'rut': '45.678.901-2', 'nombre': 'Distribuidora D Hnos', 'direccion': 'Av. Sector Industrial 2050, Los Ángeles'},
            {'rut': '56.789.012-3', 'nombre': 'Servicios E SpA', 'direccion': 'Pasaje Sur 123, Temuco'},
            {'rut': '67.890.123-4', 'nombre': 'Retail F SA', 'direccion': 'Mall Centro 1500, Puerto Varas'},
            {'rut': '78.901.234-5', 'nombre': 'Consultora G Ltda', 'direccion': 'Torre Financiera, Piso 20, Antofagasta'},
            {'rut': '89.012.345-6', 'nombre': 'Inmobiliaria H SpA', 'direccion': 'Av. Libertad 789, La Serena'},
        ]

        # Crear factores tributarios
        factores_data = [
            {'codigo': 'FT-001', 'descripcion': 'Impuesto a la Renta - Persona Natural'},
            {'codigo': 'FT-002', 'descripcion': 'Impuesto a la Renta - Empresa'},
            {'codigo': 'FT-003', 'descripcion': 'Contribución de Bienes Raíces'},
            {'codigo': 'FT-004', 'descripcion': 'IVA - Régimen General'},
            {'codigo': 'FT-005', 'descripcion': 'Timbres y Estampillas'},
        ]

        # Comentarios ficticios
        comentarios = [
            'Clasificación vigente según última declaración',
            'Contribuyente en regla al día',
            'Pendiente de verificación de documentación',
            'Requiere actualización de datos',
            'Autorizado para realizar operaciones',
            'En proceso de revisión fiscal',
            'Contribuyente con historial limpio',
            'Deuda tributaria saldada',
            'Solicitud de prórroga aprobada',
            'Contribuyente especial por volumen de operaciones',
        ]

        # Crear emisores
        created_emisores = 0
        for e_data in emisores_data:
            emisor, created = Emisor.objects.get_or_create(
                rut=e_data['rut'],
                defaults={
                    'nombre': e_data['nombre'],
                    'direccion': e_data['direccion'],
                    'activo': True
                }
            )
            if created:
                created_emisores += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Emisor creado: {e_data['nombre']}"))
            else:
                self.stdout.write(self.style.WARNING(f"- Emisor ya existe: {e_data['nombre']}"))

        # Crear factores
        created_factores = 0
        for f_data in factores_data:
            factor, created = FactorTributario.objects.get_or_create(
                codigo=f_data['codigo'],
                defaults={
                    'descripcion': f_data['descripcion'],
                    'vigente': True
                }
            )
            if created:
                created_factores += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Factor creado: {f_data['codigo']}"))
            else:
                self.stdout.write(self.style.WARNING(f"- Factor ya existe: {f_data['codigo']}"))

        # Obtener usuario para asignar calificaciones
        usuario = User.objects.filter(is_staff=True).first() or User.objects.first()

        # Crear calificaciones con comentarios
        created_calificaciones = 0
        emisores_list = list(Emisor.objects.all())
        factores_list = list(FactorTributario.objects.all())

        if emisores_list and factores_list:
            for i, emisor in enumerate(emisores_list[:5]):  # Primeros 5 emisores
                for j, factor in enumerate(factores_list[:3]):  # Primeros 3 factores
                    comentario = comentarios[(i + j) % len(comentarios)]
                    
                    calif, created = Calificacion.objects.get_or_create(
                        emisor=emisor,
                        factor=factor,
                        defaults={
                            'usuario': usuario,
                            'comentario': comentario
                        }
                    )
                    if created:
                        created_calificaciones += 1
                        self.stdout.write(self.style.SUCCESS(
                            f"✓ Calificación: {emisor.nombre} → {factor.codigo}"
                        ))

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Resumen:\n"
            f"  • {created_emisores} emisores creados\n"
            f"  • {created_factores} factores creados\n"
            f"  • {created_calificaciones} calificaciones creadas"
        ))
