from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    # el la última linea tenemos que agregar el "apps." especificando el nombre de la misma app
