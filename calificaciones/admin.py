from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Emisor, FactorTributario, BitacoraAccesos,
    CargaMasiva, HistorialAuditoria, Reporte, Calificacion
)

# Personalizar admin de Emisor para que admin pueda crear/editar
@admin.register(Emisor)
class EmisorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'direccion', 'activo', 'fecha_registro')
    list_filter = ('activo', 'fecha_registro')
    search_fields = ('rut', 'nombre')
    ordering = ('nombre',)

# El modelo User ya está registrado por defecto, pero podemos extenderlo
# Para asegurar que admin pueda crear analistas (usuarios con is_staff=True)
# Django ya lo permite por defecto en /admin/auth/user/

admin.site.register(FactorTributario)
admin.site.register(BitacoraAccesos)
admin.site.register(CargaMasiva)
admin.site.register(HistorialAuditoria)
admin.site.register(Reporte)
admin.site.register(Calificacion)
