from django.urls import resolve
from django.urls.exceptions import Resolver404
import re

class BreadcrumbsMiddleware:
    """
    Middleware para generar automáticamente las migas de pan (breadcrumbs) basadas en la URL actual.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Procesar la solicitud antes de la vista
        self.process_request(request)
        
        # Llamar a la vista
        response = self.get_response(request)
          # Retornar la respuesta
        return response
        
    def process_request(self, request):
        """
        Procesa la solicitud para añadir información de breadcrumbs.
        """
        # Inicializar la lista de breadcrumbs
        breadcrumb_items = []
        
        # Obtener la ruta actual
        path = request.path_info.strip('/')
        if not path:
            # Si estamos en la raíz, no necesitamos breadcrumbs
            request.breadcrumb_items = []
            return

        # Siempre incluir "Inicio" como primer elemento
        breadcrumb_items.append({
            'title': 'Inicio',
            'url': '/'
        })

        # Dividir la ruta en segmentos
        segments = path.split('/')
        
        # URL acumulativa para construir los enlaces
        current_url = ''
          # Asociaciones comunes de segmentos de URL a títulos descriptivos
        title_mapping = {
            'doctor': 'Sistema Médico',
            'patients': 'Pacientes',
            'medication': 'Medicamentos',
            'diagnosis': 'Diagnósticos',
            'security': 'Seguridad',
            'users': 'Usuarios',
            'groups': 'Grupos',
            'add': 'Añadir',
            'edit': 'Editar',
            'delete': 'Eliminar',
            'detail': 'Detalles',
            'list': 'Lista',
            'profile': 'Perfil',
            'settings': 'Configuración'
        }
          # Mapa de URLs especiales que deben redirigir a ubicaciones específicas
        url_redirect_mapping = {
            'doctor': '/',      # Redirigir "Sistema Médico" al home
            'security': '/',    # Redirigir "Seguridad" al home
            'patients': '/doctor/patients/',  # Enlaces directos a secciones principales
            'medication': '/doctor/medication/',
            'diagnosis': '/doctor/diagnosis/',
            'users': '/security/users/',
            'modules': '/security/modules/',
            'menus': '/security/menus/'
        }
        
        # Detectar IDs numéricos para reemplazarlos por un título genérico
        id_pattern = re.compile(r'^\d+$')
        
        for i, segment in enumerate(segments):
            current_url += f'/{segment}'
            
            # Determinar el título para este segmento
            if segment in title_mapping:
                title = title_mapping[segment]
            elif id_pattern.match(segment):
                # Si es un ID, usamos un título genérico o intentamos obtener un título más descriptivo
                title = "Elemento"
                # Aquí podrías intentar resoluciones más complejas, como consultar la base de datos
                # si el segmento anterior nos da una pista sobre qué buscar
            else:
                # Capitalizar y reemplazar guiones y subrayados por espacios
                title = segment.replace('-', ' ').replace('_', ' ').title()
              # Determinar la URL para este elemento
            url = None
            if i < len(segments) - 1:  # No es el último elemento
                # Verificar si hay una redirección especial para este segmento
                if segment in url_redirect_mapping:
                    url = url_redirect_mapping[segment]
                else:
                    url = current_url
            
            # Añadir a la lista de breadcrumbs
            breadcrumb_items.append({
                'title': title,
                'url': url  # Usar URL especial si está disponible, de lo contrario usar la URL actual
            })

        # Añadir los breadcrumbs a la solicitud para que estén disponibles en las plantillas
        request.breadcrumb_items = breadcrumb_items