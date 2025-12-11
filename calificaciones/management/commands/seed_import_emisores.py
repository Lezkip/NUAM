"""Crea emisores base para pruebas de carga masiva."""
from django.core.management.base import BaseCommand
from calificaciones.models import Emisor
from datetime import datetime

RUTS_BASE = [
    "76.123.456-7",
    "77.234.567-8",
    "78.345.678-9",
    "79.456.789-0",
    "80.567.890-1",
    "81.678.901-2",
    "82.789.012-3",
    "83.890.123-4",
    "84.901.234-5",
    "85.012.345-6",
    "86.123.456-7",
    "87.234.567-8",
    "88.345.678-9",
    "89.456.789-0",
    "90.567.890-1",
    "91.678.901-2",
    "92.789.012-3",
    "93.890.123-4",
    "94.901.234-5",
    "95.012.345-6",
]

class Command(BaseCommand):
    help = "Crea emisores de referencia para pruebas de carga masiva"

    def handle(self, *args, **options):
        creados = 0
        for idx, rut in enumerate(RUTS_BASE, start=1):
            obj, created = Emisor.objects.get_or_create(
                rut=rut,
                defaults={
                    "nombre": f"Emisor Prueba {idx}",
                    "direccion": "Sin dirección",
                    "activo": True,
                    "fecha_registro": datetime.now(),
                },
            )
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f"Emisores verificados/creados: {len(RUTS_BASE)} (nuevos: {creados})"))
