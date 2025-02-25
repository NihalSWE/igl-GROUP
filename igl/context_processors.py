# igl/context_processors.py
from .models import Logo, NavMenu, SisterConcern  # Ensure these imports are correct

def global_context(request):
    """
    Provides the active logo and navigation menus globally.
    """
    logo = Logo.objects.filter(is_active=True).first()
    menus = NavMenu.objects.filter(is_active=True)
    sister_concerns = SisterConcern.objects.all()
    
    
    
    
    # Fetch only 'title' and 'link' from SisterConcern model for footer view
    footer_sister_concerns = SisterConcern.objects.values('title', 'link')  # Get only title and link fields
    footer_sister_concerns = list(footer_sister_concerns)  # Convert queryset to list of dictionaries

    # Split into two columns dynamically for the footer
    mid_point = len(footer_sister_concerns) // 2  # Find the middle point
    column1 = footer_sister_concerns[:mid_point]  # First half for column1
    column2 = footer_sister_concerns[mid_point:]  # Second half for column2
    return {
        'logo': logo,
        'menus': menus,
        'sister_concerns': sister_concerns,
        'column1': column1,  # Added for footer
        'column2': column2,  # Added for footer
    }
