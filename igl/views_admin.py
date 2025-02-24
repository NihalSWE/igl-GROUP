from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def home_admin(request):
    return render(request, 'backend/index.html')
    

def home(request):
    admin_menus = NavMenu.objects.filter(is_active=True)  # Fetch active menus

    # Add 'admin_' prefix to each menu URL
    for menu in admin_menus:
        menu.full_url = f"admin_{menu.url}"
        print('menu url: ', menu.full_url)

    context = {
        'admin_menus': admin_menus,
    }
    
    return render(request, 'backend/home.html', context)

def dashboard(request):
    return render(request, 'backend/dashboard.html')

def aboutus(request):
    return render(request, 'backend/aboutus.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BOD, Staff
from .forms import BODForm, StaffForm

# --------- Manage Board of Directors (BOD) ---------

# View to manage Board of Directors
# Updated manage_bod view for passing director data when editing
def manage_bod(request):
    directors = BOD.objects.all()  # Fetch all directors
    director = None  # Default to None, for creating a new director
    form = BODForm()

    if request.method == 'POST':
        form = BODForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board of Director added successfully.')
            return redirect('manage_bod')  # Redirect after successful addition
    elif request.GET.get('edit'):
        # Fetch the director's data when the edit button is clicked
        slug = request.GET.get('edit')
        director = get_object_or_404(BOD, slug=slug)
        form = BODForm(instance=director)

    context = {
        'directors': directors,
        'form': form,
        'director': director,  # Pass the director's data to the template
    }
    return render(request, 'backend/manage_bod.html', context)


# View to edit Board of Director
def edit_bod(request, slug):
    director = get_object_or_404(BOD, slug=slug)  # Get director by slug
    if request.method == 'POST':
        form = BODForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board of Director updated successfully.')
            return redirect('manage_bod')  # Redirect after successful edit
    else:
        form = BODForm(instance=director)  # Pre-fill form with existing data

    context = {
        'form': form,
        'director': director,
    }
    return render(request, 'backend/manage_bod.html', context)

# View to delete Board of Director
def delete_bod(request, slug):
    director = get_object_or_404(BOD, slug=slug)  # Get the director by slug
    director.delete()  # Delete the director
    messages.success(request, 'Board of Director deleted successfully.')
    return redirect('manage_bod')  # Redirect after deletion

# --------- Manage Staff ---------

# View to manage Staff
def manage_staff(request):
    staff_members = Staff.objects.all()  # Fetch all staff members
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member added successfully.')
            return redirect('manage_staff')  # Redirect after successful addition
    else:
        form = StaffForm()

    context = {
        'staff_members': staff_members,
        'form': form,
    }
    return render(request, 'backend/manage_staff.html', context)

# View to edit Staff
def edit_staff(request, slug):
    staff = get_object_or_404(Staff, slug=slug)
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member updated successfully.')
            return redirect('manage_staff')  # Redirect after successful edit
    else:
        form = StaffForm(instance=staff)
    
    context = {
        'form': form,
        'staff': staff,
    }
    return render(request, 'backend/manage_staff.html', context)

# View to delete Staff
def delete_staff(request, slug):
    staff = get_object_or_404(Staff, slug=slug)  # Get staff member by slug
    staff.delete()  # Delete the staff member
    messages.success(request, 'Staff member deleted successfully.')
    return redirect('manage_staff')  # Redirect after deletion

