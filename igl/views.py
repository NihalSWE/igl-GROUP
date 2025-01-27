from django.shortcuts import render
from .models import CoverSection,ContactBanner, Contact_ShedulSection


# Create your views here.

def base(request):
    return render(request, 'frontend/base.html')

def home(request):
    cover_section = CoverSection.objects.first()  # Fetch the first cover section
    return render(request, 'frontend/home.html', {'cover_section': cover_section})


def about(request):
    return render(request, 'frontend/about.html')

def contact(request):
    banner = ContactBanner.objects.first()
    section = Contact_ShedulSection.objects.prefetch_related("locations").first()
    context={
        'banner':banner,
        'section':section,
    }
    return render(request, 'frontend/contact.html',context)

def gallery(request):
    return render(request, 'frontend/gallery.html')

def case_studies(request):
    return render(request, 'frontend/case-studies.html')

def igl_web(request):
    return render(request, 'frontend/igl_web.html')

def bod(request):
    return render(request, 'frontend/BOD.html')

def bos(request):
    return render(request, 'frontend/BOS.html')
