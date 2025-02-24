# igl/context_processors.py
from .models import Logo, NavMenu, SisterConcern  # Ensure these imports are correct

def global_context(request):
    """
    Provides the active logo and navigation menus globally.
    """
    logo = Logo.objects.filter(is_active=True).first()
    menus = NavMenu.objects.filter(is_active=True)
    sister_concerns = SisterConcern.objects.all()
    return {
        'logo': logo,
        'menus': menus,
        'sister_concerns': sister_concerns,
    }
