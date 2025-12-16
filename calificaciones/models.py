from django.db import models
from django.conf import settings


# ================================
# 1. EMISOR
# ================================
class Emisor(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


# ================================
# 2. FACTOR TRIBUTARIO
# ================================
class FactorTributario(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=255)
    vigente = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# ================================
# 3. CALIFICACIÓN TRIBUTARIA
# ================================
class Calificacion(models.Model):
    emisor = models.ForeignKey(Emisor, on_delete=models.CASCADE, related_name="calificaciones")
    factor = models.ForeignKey(FactorTributario, on_delete=models.PROTECT)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("emisor", "factor")
        ordering = ["-fecha_asignacion"]
        indexes = [
            models.Index(fields=["emisor", "fecha_asignacion"], name="idx_calif_emisor_fecha"),
            models.Index(fields=["factor", "fecha_asignacion"], name="idx_calif_factor_fecha"),
            models.Index(fields=["fecha_asignacion"], name="idx_calif_fecha"),
        ]

    def __str__(self):
        return f"{self.emisor} → {self.factor}"


# ================================
# 4. HISTORIAL DE AUDITORÍA
# ================================
class HistorialAuditoria(models.Model):
    ACCION_CHOICES = [
        ('CREAR', 'Crear'),
        ('EDITAR', 'Editar'),
        ('ELIMINAR', 'Eliminar'),
        ('ASIGNAR', 'Asignar'),
    ]
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES, default='EDITAR')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    emisor = models.ForeignKey(Emisor, on_delete=models.CASCADE)
    factor_anterior = models.CharField(max_length=50, null=True, blank=True)
    factor_nuevo = models.CharField(max_length=50)
    comentario_anterior = models.TextField(null=True, blank=True)
    comentario_nuevo = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Auditoría {self.emisor} ({self.fecha})"


# ================================
# 5. CARGA MASIVA
# ================================
class CargaMasiva(models.Model):
    archivo = models.FileField(upload_to="uploads/")
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    registros_procesados = models.IntegerField(default=0)
    registros_erroneos = models.IntegerField(default=0)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Carga {self.id} - {self.fecha}"


# ================================
# 6. REPORTES GENERADOS
# ================================
class Reporte(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_generado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    archivo = models.FileField(upload_to="reportes/")

    class Meta:
        ordering = ["-fecha_generado"]

    def __str__(self):
        return f"Reporte {self.nombre} ({self.fecha_generado})"


# ================================
# 7. BITÁCORA DE ACCESOS
# ================================
class BitacoraAccesos(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Acceso {self.usuario} - {self.fecha}"
