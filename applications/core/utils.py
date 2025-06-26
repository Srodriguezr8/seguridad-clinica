class BreadcrumbMixin:
    """
    Mixin para agregar breadcrumbs personalizados a las vistas.
    Esto permite tener control más preciso sobre las migas de pan en vistas específicas.
    """
    breadcrumb_title = None  # Título a mostrar en la miga de pan
    breadcrumb_url = None    # URL personalizada para la miga de pan
    
    def get_context_data(self, **kwargs):
        """Agrega información de breadcrumbs al contexto."""
        context = super().get_context_data(**kwargs)
        
        # Si hay breadcrumbs generados automáticamente, los usamos como base
        breadcrumb_items = getattr(self.request, 'breadcrumb_items', [])
        
        # Si hay un breadcrumb_title personalizado, reemplazamos el último elemento
        if self.breadcrumb_title and breadcrumb_items:
            last_item = breadcrumb_items[-1].copy()
            last_item['title'] = self.breadcrumb_title
            if self.breadcrumb_url:
                last_item['url'] = self.breadcrumb_url
            breadcrumb_items[-1] = last_item
        
        context['breadcrumb_items'] = breadcrumb_items
        return context

def custom_breadcrumbs(request, items):
    """
    Función para definir breadcrumbs personalizados en una vista basada en función.
    
    Args:
        request: La request de Django
        items: Lista de diccionarios con 'title' y 'url' para cada elemento
    """
    request.breadcrumb_items = items