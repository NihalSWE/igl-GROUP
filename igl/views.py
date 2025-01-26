from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'frontend/base.html')

def home(request):
    return render(request, 'frontend/home.html')


def about(request):
    return render(request, 'frontend/about.html')

def contact(request):
    return render(request, 'frontend/contact.html')

