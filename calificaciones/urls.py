from django.urls import path
from . import views

urlpatterns = [
    # ==============================
    # 0. DASHBOARD
    # ==============================
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # ==============================
    # 1. EMISORES (CRUD Completo)
    # ==============================
    path("emisores/", views.lista_emisores, name="lista_emisores"),
    path("emisores/nuevo/", views.emisor_create, name="emisor_create"),
    path("emisores/<int:pk>/editar/", views.emisor_update, name="emisor_update"),
    path("emisores/<int:pk>/eliminar/", views.emisor_delete, name="emisor_delete"),
    path("emisores/detalle/<int:id>/", views.detalle_emisor, name="detalle_emisor"),

    # ==============================
    # 2. FACTORES (CRUD Completo)
    # ==============================
    path("factores/", views.lista_factores, name="lista_factores"),
    path("factores/nuevo/", views.factor_create, name="factor_create"),
    path("factores/<int:pk>/editar/", views.factor_update, name="factor_update"),
    path("factores/<int:pk>/eliminar/", views.factor_delete, name="factor_delete"),
    path("factores/detalle/<int:id>/", views.detalle_factor, name="detalle_factor"),

    # ==============================
    # 3. CALIFICACIONES (CRUD)
    # ==============================
    # Nota: views.lista_calificaciones renderiza el HTML principal
    path("calificaciones/", views.lista_calificaciones, name="calificacion_list"),
    path("calificaciones/nueva/", views.calificacion_create, name="calificacion_create"),
    path("calificaciones/<int:pk>/editar/", views.calificacion_update, name="calificacion_update"),
    path("calificaciones/<int:pk>/eliminar/", views.calificacion_delete, name="calificacion_delete"),
    
    # API para detalles (AJAX)
    path("calificaciones/api/<int:id>/", views.detalle_calificacion, name="detalle_calificacion_api"),

    # ==============================
    # 4. CARGA MASIVA
    # ==============================
    path("calificaciones/carga-masiva/", views.carga_masiva_calificaciones, name="carga_masiva_calificaciones"),
    path("api/carga-masiva/", views.api_carga_masiva, name="api_carga_masiva"),
    
    # ==============================
    # 5. AUDITORÍA
    # ==============================
    path("auditoria/", views.lista_auditoria, name="lista_auditoria"),
    
    # ==============================
    # 6. GESTIÓN DE USUARIOS (Admin)
    # ==============================
    path("usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/eliminar/<int:user_id>/", views.eliminar_usuario, name="eliminar_usuario"),
]