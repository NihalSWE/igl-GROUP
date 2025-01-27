# igl/context_processors.py
from .models import Logo, NavMenu  # Ensure these imports are correct

def global_context(request):
    """
    Provides the active logo and navigation menus globally.
    """
    logo = Logo.objects.filter(is_active=True).first()
    menus = NavMenu.objects.filter(is_active=True)
    return {
        'logo': logo,
        'menus': menus,
    }
