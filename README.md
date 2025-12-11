# Proyecto NUAM - Calificaciones

Aplicación Django para gestionar emisores, factores tributarios y calificaciones con auditoría de cambios y carga masiva.

## Requisitos
- Python 3.11+ (recomendado)
- PostgreSQL 13+ (base de datos `nuam_db` por defecto)
- pip

## Instalación rápida (PowerShell)
```powershell
python -m venv env
./env/Scripts/Activate.ps1
pip install -r requirements.txt
```

## Configuración
Las credenciales por defecto viven en `proyecto_nuam/settings.py` (DB `nuam_db`, usuario `postgres`, password `1234`). Ajusta esos valores si tu entorno difiere. Para producción, mueve `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y los datos de BD a variables de entorno o a un `.env` que no se comparta.

## Migraciones y superusuario
```powershell
python manage.py migrate
python manage.py createsuperuser
```

## Ejecutar
```powershell
python manage.py runserver
```
Abre http://127.0.0.1:8000/

## URLs principales
- `/accounts/login/` : login (Django auth)
- `/dashboard/` : panel principal
- `/api/` : rutas de la app `calificaciones` (CRUD de emisores, factores, calificaciones, auditoría, usuarios, carga masiva)
- `/auditoria/` : historial de cambios (solo staff/superusuario)
- `/admin/` : admin de Django

## Notas
- La sesión expira por inactividad (30 min) según `SESSION_COOKIE_AGE`.
- Middleware de no-cache evita mostrar páginas protegidas al usar botón atrás después de logout.
- Carga masiva de calificaciones requiere archivos compatibles (ver formularios en la UI).

## Despliegue
- Configura variables de entorno para SECRET_KEY, DEBUG=False, ALLOWED_HOSTS y credenciales de BD.
- Aplica migraciones, crea un usuario administrador y configura `STATIC_ROOT` si usas `collectstatic`.
