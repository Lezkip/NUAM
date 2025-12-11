from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Calificacion, HistorialAuditoria

@receiver(pre_save, sender=Calificacion)
def calificacion_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Calificacion.objects.get(pk=instance.pk)
            instance._original_factor = original.factor
        except Calificacion.DoesNotExist:
            instance._original_factor = None
    else:
        instance._original_factor = None

@receiver(post_save, sender=Calificacion)
def calificacion_post_save(sender, instance, created, **kwargs):
    factor_anterior = getattr(instance, '_original_factor', None)
    factor_nuevo = instance.factor
    if created:
        HistorialAuditoria.objects.create(
            usuario=instance.usuario,
            emisor=instance.emisor,
            factor_anterior=str(factor_anterior) if factor_anterior else None,
            factor_nuevo=str(factor_nuevo),
        )
    else:
        if factor_anterior != factor_nuevo:
            HistorialAuditoria.objects.create(
                usuario=instance.usuario,
                emisor=instance.emisor,
                factor_anterior=str(factor_anterior) if factor_anterior else None,
                factor_nuevo=str(factor_nuevo),
            )
