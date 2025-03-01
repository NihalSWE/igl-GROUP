from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from PIL import Image
from django import forms
from .forms import StaffForm,BODForm
import os
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings



from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Only allow superusers
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid credentials or not an admin user.")

    return render(request, 'backend/admin_login.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page

# Dashboard View (Only accessible if logged in)
@login_required
def dashboard(request):
    return render(request, 'backend/admin_dashboard.html')







def admin_home(request):
    return render(request, 'backend/base.html')


def admin_home_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        title = request.POST.get('button_text', '').strip()
        description = request.POST.get('description', '').strip()
        banner_image = request.FILES.get('banner_image')

        # Basic validation: ensure required fields are provided.
        if not title or not description or not banner_image:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_home_banner')  # Change to your URL name
        try:
            # Create a new HomeBanner instance. 
            # We leave button_text and url empty or provide default values.
            banner = HomeBanner(
                title=title,
                description=description,
                button_text='',  # Set default if not provided
                url='',          # Set default if not provided
                background_image=banner_image
            )
            banner.save()
            messages.success(request, "Banner added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('admin_home_banner')
    
    return render(request, 'backend/admin_home_banner.html')



def home_banner_list(request):
    banners = HomeBanner.objects.all()
    return render(request, 'backend/home_banner_list.html', {'banners': banners})

# Edit Home Banner
def edit_home_banner(request, banner_id):
    banner = get_object_or_404(HomeBanner, id=banner_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        button_text = request.POST.get('button_text', '').strip()
        description = request.POST.get('description', '').strip()
        banner_image = request.FILES.get('banner_image', banner.background_image)  # Default to current image if not provided
        
        if not title or not description:
            messages.error(request, "Please fill in all required fields.")
            return redirect('edit_home_banner', banner_id=banner.id)
        
        try:
            # Update banner details
            banner.title = title
            banner.button_text = button_text
            banner.description = description
            banner.background_image = banner_image
            banner.save()
            messages.success(request, "Banner updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('home_banner_list')  # Redirect to list view
    
    return render(request, 'backend/edit_home_banner.html', {'banner': banner})

# Delete Home Banner
def delete_home_banner(request, banner_id):
    banner = get_object_or_404(HomeBanner, id=banner_id)
    
    try:
        banner.delete()
        messages.success(request, "Banner deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('home_banner_list')  # Redirect to list view


def home_intro_form(request):
# Fetch the first HomeIntro object if it exists
    home_intro = HomeIntro.objects.first()  

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image1 = request.FILES.get('image1')  # New image
        progress1_title = request.POST.get('progress1_title', '').strip()
        progress1_value = request.POST.get('progress1_value', '').strip()
        progress2_title = request.POST.get('progress2_title', '').strip()
        progress2_value = request.POST.get('progress2_value', '').strip()

        # Validate required fields
        if not title or not description or not progress1_title or not progress1_value or not progress2_title or not progress2_value:
            messages.error(request, "Please fill in all required fields.")
            return redirect('home_intro_form')

        try:
            progress1_value = int(progress1_value)
            progress2_value = int(progress2_value)
        except ValueError:
            messages.error(request, "Progress values must be valid numbers.")
            return redirect('home_intro_form')

        try:
            if home_intro:
                # Update existing record
                home_intro.title = title
                home_intro.description = description
                if image1:
                    home_intro.image1 = image1  # Only update if new image is uploaded
                home_intro.progress1_title = progress1_title
                home_intro.progress1_value = progress1_value
                home_intro.progress2_title = progress2_title
                home_intro.progress2_value = progress2_value
                home_intro.save()
                messages.success(request, "Home Intro updated successfully!")
            else:
                # Create a new record
                HomeIntro.objects.create(
                    title=title,
                    description=description,
                    image1=image1,
                    progress1_title=progress1_title,
                    progress1_value=progress1_value,
                    progress2_title=progress2_title,
                    progress2_value=progress2_value
                )
                messages.success(request, "Home Intro saved successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('home_intro_form')

    context = {
        'home_intro': home_intro,
    }

    return render(request, 'backend/home_intro_form.html', context)


def industry_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        icon = request.FILES.get('icon')
        link = request.POST.get('link', '').strip()

        # Validate the required field
        if not name:
            messages.error(request, "Please enter the Industry name.")
            return redirect('add_industry')  # Update with your URL name

        try:
            industry = Industry(
                name=name,
                icon=icon,  # icon is optional
                link=link   # link is optional
            )
            industry.save()
            messages.success(request, "Industry saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('industry_form')  # Change to your desired URL

    # For GET requests, render the form template.
    return render(request, 'backend/industry_form.html')


def industry_list(request):
    industries = Industry.objects.all()  # Retrieve all industries
    context = {
        'industries': industries,
    }
    return render(request, 'backend/industry_list.html', context)


def edit_industry(request, industry_id):
    industry = get_object_or_404(Industry, pk=industry_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        icon = request.FILES.get('icon', industry.icon)  # Use current icon if not provided
        link = request.POST.get('link', '').strip()

        # Validate the required field
        if not name:
            messages.error(request, "Please enter the Industry name.")
            return redirect('edit_industry', industry_id=industry.id)

        try:
            # Update the industry record
            industry.name = name
            industry.icon = icon
            industry.link = link
            industry.save()
            messages.success(request, "Industry updated successfully!")
            return redirect('industry_list')  # Redirect to the list view
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    
    context = {
        'industry': industry,
    }
    return render(request, 'backend/edit_industry.html', context)


def delete_industry(request, industry_id):
    industry = get_object_or_404(Industry, pk=industry_id)
    
    try:
        industry.delete()
        messages.success(request, "Industry deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('industry_list')  # Redirect to the list view








def reason_to_choose_list(request):
    reasons = ReasonToChooseUs.objects.all().order_by('order')
    context = {
        'reasons': reasons,
    }
    return render(request, 'backend/reason_to_choose_list.html', context)



def edit_reason_to_choose(request, reason_id):
    reason = get_object_or_404(ReasonToChooseUs, pk=reason_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', reason.icon)  # default to current icon if not provided
        order = request.POST.get('order', '0').strip()

        # Validate required fields
        if not title or not description:
            messages.error(request, "Title and Description are required.")
            return redirect('edit_reason_to_choose', reason_id=reason.id)

        try:
            order_int = int(order)
        except ValueError:
            messages.error(request, "Order must be a valid number.")
            return redirect('edit_reason_to_choose', reason_id=reason.id)

        # Update the record
        reason.title = title
        reason.description = description
        reason.icon = icon
        reason.order = order_int
        reason.save()
        messages.success(request, "Reason to Choose Us updated successfully!")
        return redirect('reason_to_choose_list')  # Redirect to list view
    
    context = {
        'reason': reason,
        'form_icon_choices': ReasonToChooseUs.ICON_CHOICES,
    }
    return render(request, 'backend/edit_reason_to_choose.html', context)

def delete_reason_to_choose(request, reason_id):
    reason = get_object_or_404(ReasonToChooseUs, pk=reason_id)
    
    try:
        reason.delete()
        messages.success(request, "Reason to Choose Us deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('reason_to_choose_list')  # Redirect to list view


def add_reason_to_choose(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', '🎯')  # default to "🎯" if not provided
        order = request.POST.get('order', '0').strip()

        # Validate required fields
        if not title or not description:
            messages.error(request, "Title and Description are required.")
            return redirect('add_reason_to_choose')  # Update with your URL name

        try:
            order_int = int(order)
        except ValueError:
            messages.error(request, "Order must be a valid number.")
            return redirect('add_reason_to_choose')

        try:
            reason = ReasonToChooseUs(
                title=title,
                description=description,
                icon=icon,
                order=order_int,
            )
            reason.save()
            messages.success(request, "Reason to Choose Us added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('add_reason_to_choose')  # Change to your desired URL
    
    context = {
        'form_icon_choices': ReasonToChooseUs.ICON_CHOICES,
    }

    return render(request, 'backend/add_reason_to_choose.html', context)

# View to manage WeServe objects (Display)
# View to display the manage WeServe page
def manage_we_serves(request):
    we_serves = WeServe.objects.all()  # Get all WeServe records
    return render(request, 'backend/manage_weserve.html', {'we_serves': we_serves})

# View to add a new WeServe
def add_we_serve(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.FILES.get('icon')

        # Create a new WeServe instance and save it
        new_we_serve = WeServe(name=name, icon=icon)
        new_we_serve.save()

        return JsonResponse({"success": True, "message": "WeServe added successfully."})
    
    return JsonResponse({"success": False, "message": "Invalid request method."})

# View to edit an existing WeServe
def edit_we_serve(request, id):
    try:
        we_serve = WeServe.objects.get(id=id)
        if request.method == 'POST':
            we_serve.name = request.POST.get('name')
            if 'icon' in request.FILES:
                we_serve.icon = request.FILES.get('icon')
            we_serve.save()

            return JsonResponse({"success": True, "message": "WeServe updated successfully."})
        else:
            return JsonResponse({"success": False, "message": "Invalid request method."})
    except WeServe.DoesNotExist:
        return JsonResponse({"success": False, "message": "WeServe not found."})

# View to delete a WeServe
def delete_we_serve(request, id):
    try:
        we_serve = WeServe.objects.get(id=id)
        we_serve.delete()
        return JsonResponse({"success": True, "message": "WeServe deleted successfully."})
    except WeServe.DoesNotExist:
        return JsonResponse({"success": False, "message": "WeServe not found."})





def about_banner_form(request):
    # Check if there is an existing banner or if it's a new form
    try:
        banner = AboutBanner.objects.first()  # Get the first banner (or None if no banner exists)
    except AboutBanner.DoesNotExist:
        banner = None
    
    if request.method == 'POST':
        # Title is optional since it has a default value, but you can allow users to update it.
        title = request.POST.get('title', '').strip() or "About Us"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is provided
        if not background_image and not banner:
            messages.error(request, "Please upload a background image.")
            return redirect('add_about_banner')  # Replace with your URL name

        try:
            if banner:
                # Update existing banner if it exists
                banner.title = title
                if background_image:
                    banner.background_image = background_image
            else:
                # Create new banner if none exists
                banner = AboutBanner(
                    title=title,
                    background_image=background_image
                )
            banner.save()

            messages.success(request, "About Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('about_banner_form')  # Change this to your desired URL

    # Pass the banner object to the template if it exists
    return render(request, 'backend/about_banner_form.html', {'banner': banner})

def about_section_form(request):
    about_section = AboutSection.objects.first()  # Or filter by any condition to get the specific record

    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        # Validate that description is provided.
        if not description:
            messages.error(request, "Please provide a description.")
            return redirect('add_about_section')  # Update with your URL name

        try:
            if about_section:
                # Update the existing about section if it exists
                about_section.description = description
                about_section.image = image  # Update the image if it's provided
                about_section.save()
            else:
                # Create a new AboutSection if one doesn't exist
                about_section = AboutSection(
                    description=description,
                    image=image  # image is optional
                )
                about_section.save()
                
            messages.success(request, "About Section saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('about_section_form')

    # Pass the existing about_section to the template
    return render(request, 'backend/about_section_form.html', {'about_section': about_section})



def gallery_banner_form(request):
    # Default values in case of an empty GET request (new banner form)
    banner = None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip() or "Contact Us"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is uploaded
        if not background_image:
            messages.error(request, "Please upload a background image.")
            return redirect('add_gallery_banner')  # Replace with your URL name

        try:
            banner = GalleryBanner(
                title=title,
                background_image=background_image
            )
            banner.save()
            messages.success(request, "Gallery Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('gallery_banner_form')  # Change to your desired URL

    else:
        # In case the page was loaded with a GET request (e.g. to edit the banner)
        banner = GalleryBanner.objects.first()  # You can modify this to fetch a specific banner if needed

    return render(request, 'backend/gallery_banner_form.html', {'banner': banner})


def gallery_album_form(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        thumbnail = request.FILES.get('thumbnail')

        try:
            album = Gallery_Album(
                title=title if title else None,
                thumbnail=thumbnail  # Thumbnail is optional
            )
            album.save()
            messages.success(request, "Gallery album saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('gallery_album_form')  # Replace with your URL name

    return render(request, 'backend/gallery_album_form.html')

def gallery_album_list(request):
    albums = Gallery_Album.objects.all()
    return render(request, 'backend/gallery_album_list.html', {'albums': albums})



def gallery_album_edit(request, album_id):
    album = get_object_or_404(Gallery_Album, id=album_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        thumbnail = request.FILES.get('thumbnail')

        try:
            album.title = title if title else None
            if thumbnail:
                album.thumbnail = thumbnail
            album.save()

            messages.success(request, "Gallery album updated successfully!")
            return redirect('gallery_album_list')  # Redirect to the list page
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'backend/gallery_album_edit.html', {'album': album})


def gallery_album_delete(request, album_id):
    album = get_object_or_404(Gallery_Album, id=album_id)
    
    try:
        album.delete()
        messages.success(request, "Gallery album deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('gallery_album_list')  # Redirect to the album list page


def gallery_album_details(request):
    albums = Gallery_Album.objects.all()  # Fetch all albums
    
    if request.method == "POST":
        album_id = request.POST.get("album", "").strip()
        image = request.FILES.get("image")

        try:
            if album_id and image:
                album = Gallery_Album.objects.get(id=album_id)  # Fetch the album
                gallery_image = Gallery_AlbumDetails(album=album, image=image)
                gallery_image.save()
                messages.success(request, "Gallery album image saved successfully!")
            else:
                messages.error(request, "Please select an album and upload an image.")
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect("gallery_album_details")  # Redirect after saving

    return render(request, "backend/gallery_album_details.html", {"albums": albums})

def gallery_album_details_list(request):
    # Fetch all album details (images of the albums)
    album_details = Gallery_AlbumDetails.objects.all() 

    return render(request, "backend/gallery_album_details_list.html", {
        "album_details": album_details
    })


def edit_gallery_album_detail(request, detail_id):
    # Fetch the album detail (image) to be edited
    album_detail = get_object_or_404(Gallery_AlbumDetails, id=detail_id)

    if request.method == 'POST':
        # Check if a new image is provided, if so update it
        new_image = request.FILES.get('image')
        if new_image:
            album_detail.image = new_image  # Update the image if provided

        try:
            album_detail.save()
            messages.success(request, "Gallery album image updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect("gallery_album_details_list")  # Redirect to the list view after saving

    return render(request, "backend/edit_gallery_album_detail.html", {
        "album_detail": album_detail
    })



def delete_gallery_album_detail(request, detail_id):
    try:
        album_detail = get_object_or_404(Gallery_AlbumDetails, id=detail_id)
        album_detail.delete()
        messages.success(request, "Gallery album image deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect("gallery_album_details_list")

def career_image_list(request):
    career_images = CareerImages.objects.all()
    return render(request, 'backend/career_image_list.html', {'career_images': career_images})


def career_banner_form(request):
    # Check if there is an existing banner or if it's a new form
    try:
        banner = CareerBanner.objects.first()  # Get the first banner (or None if no banner exists)
    except CareerBanner.DoesNotExist:
        banner = None
    
    if request.method == 'POST':
        # Title is optional since it has a default value, but you can allow users to update it.
        title = request.POST.get('title', '').strip() or "Career"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is provided
        if not background_image and not banner:
            messages.error(request, "Please upload a background image.")
            return redirect('career_banner_form')  # Change to correct URL name

        try:
            if banner:
                # Update existing banner if it exists
                banner.title = title
                if background_image:
                    banner.background_image = background_image
            else:
                # Create new banner if none exists
                banner = CareerBanner(
                    title=title,
                    background_image=background_image
                )
            banner.save()

            messages.success(request, "Career Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('career_banner_form')  # Redirect back to the form page

    # Pass the banner object to the template if it exists
    return render(request, 'backend/career_banner_form.html', {'banner': banner})

@csrf_exempt
def career_images(request):
    if request.method == "POST":
        main_image = request.FILES.get("main_image")
        group_image = request.FILES.get("group_image")
        activity_image1 = request.FILES.get("activity_image1")
        activity_image2 = request.FILES.get("activity_image2")
        is_active = request.POST.get("is_active") == "on"
        image_id = request.POST.get("image_id")  # Get image_id from POST for editing

        if image_id:  # If image_id is present, we're editing
            image = get_object_or_404(CareerImages, id=image_id)
            image.main_image = main_image
            image.group_image = group_image
            image.activity_image1 = activity_image1
            image.activity_image2 = activity_image2
            image.is_active = is_active
            image.save()
        else:  # New image creation
            CareerImages.objects.create(
                main_image=main_image,
                group_image=group_image,
                activity_image1=activity_image1,
                activity_image2=activity_image2,
                is_active=is_active,
            )

        return redirect("career_images")  # Redirect after upload or update

    # Fetch images for display
    career_images = CareerImages.objects.all()
    return render(request, "backend/career_images.html", {"career_images": career_images})

def delete_career_image(request, id):
    # Fetch the career image by ID and delete it
    image = get_object_or_404(CareerImages, id=id)
    image.delete()
    
    # Redirect to the career images listing page
    return redirect('career_images')


def edit_career_image(request, id):
    image = get_object_or_404(CareerImages, id=id)
    data = {
        'id': image.id,
        'main_image': image.main_image.url if image.main_image else None,
        'group_image': image.group_image.url if image.group_image else None,
        'activity_image1': image.activity_image1.url if image.activity_image1 else None,
        'activity_image2': image.activity_image2.url if image.activity_image2 else None,
        'is_active': image.is_active,
    }
    return JsonResponse(data)




def job_posting_list(request):
    jobs = JobPosting.objects.all()
    return render(request, 'backend/job_posting_list.html', {'jobs': jobs})

# View to add a new job posting
@csrf_exempt  # Use csrf_exempt if you're testing without CSRF protection, otherwise use proper CSRF tokens
def add_job_posting(request):
    if request.method == "POST":
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        full_description = request.POST.get('full_description')
        location = request.POST.get('location')
        department = request.POST.get('department')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')

        # Create the new job posting
        job = JobPosting.objects.create(
            title=title,
            short_description=short_description,
            full_description=full_description,
            location=location,
            department=department,
            job_type=job_type,
            salary=salary,
            deadline=deadline,
            is_active=True  # Defaulting to True or as needed
        )

        return JsonResponse({"status": "success", "message": "Job posting added successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})


# View to edit an existing job posting

@csrf_exempt
def edit_job_posting(request, id):
    job = get_object_or_404(JobPosting, id=id)

    if request.method == "GET":  # Ensure it's handling GET requests for fetching data
        # Return the job details as JSON
        return JsonResponse({
            "status": "success",
            "job": {
                "id": job.id,
                "title": job.title,
                "short_description": job.short_description,
                "full_description": job.full_description,
                "location": job.location,
                "department": job.department,
                "job_type": job.job_type,
                "salary": job.salary,
                "deadline": job.deadline,
                "is_active": job.is_active,
            }
        })

    elif request.method == "POST":
        job.title = request.POST.get('title')
        job.short_description = request.POST.get('short_description')
        job.full_description = request.POST.get('full_description')
        job.location = request.POST.get('location')
        job.department = request.POST.get('department')
        job.job_type = request.POST.get('job_type')
        job.salary = request.POST.get('salary')
        job.deadline = request.POST.get('deadline')
        job.is_active = request.POST.get('is_active') == 'on'

        job.save()

        return JsonResponse({"status": "success", "message": "Job posting updated successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})


# View to delete an existing job posting
@csrf_exempt
def delete_job_posting(request, id):
    job = get_object_or_404(JobPosting, id=id)
    
    if request.method == "POST":
        job.delete()
        return JsonResponse({"status": "success", "message": "Job posting deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})

@csrf_exempt
def delete_job_posting(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    if request.method == "POST":
        job.delete()
        return JsonResponse({"status": "success", "message": "Job posting deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})




def job_application_list(request):
    applications = JobApplication.objects.all()
    jobs = JobPosting.objects.all()
    return render(request, 'backend/job_application_list.html', {'applications': applications, 'jobs': jobs})

@csrf_exempt
def add_job_application(request):
    if request.method == "POST":
        job = get_object_or_404(JobPosting, id=request.POST.get('job'))
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cv = request.FILES.get('cv')
        linkedin_url = request.POST.get('linkedin_url', '')
        portfolio_url = request.POST.get('portfolio_url', '')
        gender = request.POST.get('gender', 'male')
        image = request.FILES.get('image')

        application = JobApplication.objects.create(
            job=job,
            name=name,
            email=email,
            phone=phone,
            cv=cv,
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url,
            gender=gender,
            image=image
        )

        return JsonResponse({"status": "success", "message": "Job application added successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})

@csrf_exempt
def edit_job_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == "POST":
        application.name = request.POST.get('name')
        application.email = request.POST.get('email')
        application.phone = request.POST.get('phone')
        application.linkedin_url = request.POST.get('linkedin_url', '')
        application.portfolio_url = request.POST.get('portfolio_url', '')
        application.gender = request.POST.get('gender', 'male')

        if 'cv' in request.FILES:
            application.cv = request.FILES['cv']
        if 'image' in request.FILES:
            application.image = request.FILES['image']

        application.save()

        return JsonResponse({"status": "success", "message": "Job application updated successfully!"})

    elif request.method == "GET":
        return JsonResponse({
            "status": "success",
            "application": {
                "id": application.id,
                "name": application.name,
                "email": application.email,
                "phone": application.phone,
                "linkedin_url": application.linkedin_url,
                "portfolio_url": application.portfolio_url,
                "gender": application.gender,
                "cv": application.cv.url if application.cv else "",
                "image": application.image.url if application.image else ""
            }
        })

    return JsonResponse({"status": "error", "message": "Invalid request method!"})

@csrf_exempt
def delete_job_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == "POST":
        application.delete()
        return JsonResponse({"status": "success", "message": "Job application deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})

def our_team_banner_form(request):
    # Check if there is an existing banner or if it's a new form
    try:
        banner = OurTeamBanner.objects.first()  # Get the first banner (or None if no banner exists)
    except OurTeamBanner.DoesNotExist:
        banner = None
    
    if request.method == 'POST':
        # Title is optional since it has a default value, but you can allow users to update it.
        title = request.POST.get('title', '').strip() or "Our Team"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is provided
        if not background_image and not banner:
            messages.error(request, "Please upload a background image.")
            return redirect('add_our_team_banner')  # Replace with your URL name

        try:
            if banner:
                # Update existing banner if it exists
                banner.title = title
                if background_image:
                    banner.background_image = background_image
            else:
                # Create new banner if none exists
                banner = OurTeamBanner(
                    title=title,
                    background_image=background_image
                )
            banner.save()

            messages.success(request, "Our Team Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('our_team_banner_form')  # Change this to your desired URL

    # Pass the banner object to the template if it exists
    return render(request, 'backend/our_team_banner_form.html', {'banner': banner})

# Updated manage_bod view for passing director data when editing
def manage_bod(request):
    directors = BOD.objects.all().order_by('-id')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle edit action
        if action == 'edit':
            director_id = request.POST.get('director_id')
            director = get_object_or_404(BOD, id=director_id)
            
            # Update director fields
            director.name = request.POST.get('name')
            director.role = request.POST.get('role')
            director.bio = request.POST.get('bio')
            director.portfolio_link = request.POST.get('portfolio_link')
            director.pdf = request.POST.get('pdf')
            
            # Handle image upload only if a new image is provided
            if 'image' in request.FILES:
                director.image = request.FILES['image']
                
            director.save()
            messages.success(request, 'Director updated successfully!')
            
        # Handle add action
        else:
            name = request.POST.get('name')
            role = request.POST.get('role')
            bio = request.POST.get('bio')
            portfolio_link = request.POST.get('portfolio_link')
            pdf = request.POST.get('pdf')
            
            # Create slug from name
            slug = slugify(name)
            
            # Check for existing director with same slug
            existing_slug_count = BOD.objects.filter(slug__startswith=slug).count()
            if existing_slug_count > 0:
                slug = f"{slug}-{existing_slug_count + 1}"
                
            # Create new director
            director = BOD(
                name=name,
                role=role,
                bio=bio,
                portfolio_link=portfolio_link,
                pdf=pdf,
                slug=slug
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                director.image = request.FILES['image']
                
            director.save()
            messages.success(request, 'Director added successfully!')
        
        return redirect('manage_bod')
            
    context = {
        'directors': directors,
    }
    return render(request, 'backend/manage_bod.html', context)

def delete_bod(request, slug):
    director = get_object_or_404(BOD, slug=slug)
    director_name = director.name
    director.delete()
    
    messages.success(request, f'Director {director_name} deleted successfully!')
    return redirect('manage_bod')
# --------- Manage Staff ---------
# Updated manage_bod view for passing director data when editing
def manage_staff(request):
    staffs = Staff.objects.all().order_by('-id')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle edit action
        if action == 'edit':
            staff_id = request.POST.get('staff_id')
            staff = get_object_or_404(Staff, id=staff_id)
            
            # Update staff fields
            staff.name = request.POST.get('name')
            staff.position = request.POST.get('position')
            staff.bio = request.POST.get('bio')
            staff.portfolio_link = request.POST.get('portfolio_link')
            staff.pdf = request.POST.get('pdf')
            
            # Handle image upload only if a new image is provided
            if 'image' in request.FILES:
                staff.image = request.FILES['image']
                
            staff.save()
            messages.success(request, 'Staff updated successfully!')
            
        # Handle add action
        else:
            name = request.POST.get('name')
            position = request.POST.get('position')
            bio = request.POST.get('bio')
            portfolio_link = request.POST.get('portfolio_link')
            pdf = request.POST.get('pdf')
            
            # Create slug from name
            slug = slugify(name)
            
            # Check for existing director with same slug
            existing_slug_count = Staff.objects.filter(slug__startswith=slug).count()
            if existing_slug_count > 0:
                slug = f"{slug}-{existing_slug_count + 1}"
                
            # Create new director
            staff = Staff(
                name=name,
                position=position,
                bio=bio,
                portfolio_link=portfolio_link,
                pdf=pdf,
                slug=slug
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                staff.image = request.FILES['image']
                
            staff.save()
            messages.success(request, 'Staff added successfully!')
        
        return redirect('manage_staff')
            
    context = {
        'staffs': staffs,
    }
    return render(request, 'backend/manage_staff.html', context)

def delete_staff(request, slug):
    staff = get_object_or_404(Staff, slug=slug)
    staff_name = staff.name
    staff.delete()
    
    messages.success(request, f'Staff {staff_name} deleted successfully!')
    return redirect('manage_staff')

# View to manage Staff
# def manage_staff(request):
#     staff_members = Staff.objects.all()  # Fetch all staff members
#     if request.method == 'POST':
#         form = StaffForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Staff member added successfully.')
#             return redirect('manage_staff')  # Redirect after successful addition
#     else:
#         form = StaffForm()
#     context = {
#         'staff_members': staff_members,
#         'form': form,
#     }
#     return render(request, 'backend/manage_staff.html', context)
# # View to edit Staff
# def edit_staff(request, slug):
#     staff = get_object_or_404(Staff, slug=slug)
#     if request.method == 'POST':
#         form = StaffForm(request.POST, request.FILES, instance=staff)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Staff member updated successfully.')
#             return redirect('manage_staff')  # Redirect after successful edit
#     else:
#         form = StaffForm(instance=staff)
#     context = {
#         'form': form,
#         'staff': staff,
#     }
#     return render(request, 'backend/manage_staff.html', context)
# # View to delete Staff
# def delete_staff(request, slug):
#     staff = get_object_or_404(Staff, slug=slug)  # Get staff member by slug
#     staff.delete()  # Delete the staff member
#     messages.success(request, 'Staff member deleted successfully.')
#     return redirect('manage_staff')  # Redirect after deletion



def location_list(request):
    locations = Contact_Location.objects.all()
    return render(request, 'backend/location_list.html', {'locations': locations})

@csrf_exempt
def add_location(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        address = request.POST.get('address')
        map_url = request.POST.get('map_url')
        phone_number = request.POST.get('phone_number')
        image = request.FILES.get('image')  # Handling image upload

        # Create the location
        new_location = Contact_Location.objects.create(
            city=city,
            address=address,
            map_url=map_url,
            phone_number=phone_number,
            image=image
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Location added successfully!',
            'location': {
                'id': new_location.id,
                'city': new_location.city,
                'address': new_location.address,
                'phone_number': new_location.phone_number
            }
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})


import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def edit_location(request, id):
    try:
        location = Contact_Location.objects.get(id=id)
    except Contact_Location.DoesNotExist:
        logger.error(f"Location with ID {id} not found.")
        return JsonResponse({'status': 'error', 'message': 'Location not found!'})
    
    if request.method == 'GET':
        # Return location details for the edit form
        return JsonResponse({
            'status': 'success',
            'location': {
                'id': location.id,
                'city': location.city,
                'address': location.address,
                'phone_number': location.phone_number,
                'map_url': location.map_url,
                'image': location.image.url if location.image else None
            }
        })
    
    if request.method == 'POST':
        # Handle the POST request for updating the location
        location.city = request.POST.get('city', location.city)
        location.address = request.POST.get('address', location.address)
        location.map_url = request.POST.get('map_url', location.map_url)
        location.phone_number = request.POST.get('phone_number', location.phone_number)

        # Handle file upload if new image is provided
        new_image = request.FILES.get('image')
        if new_image:
            location.image = new_image

        location.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Location updated successfully!',
            'location': {
                'id': location.id,
                'city': location.city,
                'address': location.address,
                'phone_number': location.phone_number
            }
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})


@csrf_exempt
def delete_location(request, id):
    try:
        location = Contact_Location.objects.get(id=id)
    except Contact_Location.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Location not found!'})

    if request.method == 'POST':
        location.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Location deleted successfully!'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})


def contact_banner_form(request):
    # Check if there is an existing banner or if it's a new form
    try:
        banner = ContactBanner.objects.first()  # Get the first banner (or None if no banner exists)
    except ContactBanner.DoesNotExist:
        banner = None
    
    if request.method == 'POST':
        # Title is optional since it has a default value, but you can allow users to update it.
        title = request.POST.get('title', '').strip() or "Contact Us"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is provided
        if not background_image and not banner:
            messages.error(request, "Please upload a background image.")
            return redirect('contact_banner_form')  # Change to correct URL name

        try:
            if banner:
                # Update existing banner if it exists
                banner.title = title
                if background_image:
                    banner.background_image = background_image
            else:
                # Create new banner if none exists
                banner = ContactBanner(
                    title=title,
                    background_image=background_image
                )
            banner.save()

            messages.success(request, "Contact Us Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('contact_banner_form')  # Redirect back to the form page

    # Pass the banner object to the template if it exists
    return render(request, 'backend/contact_banner_form.html', {'banner': banner})



def contact_list(request):
    contacts = Contact_fromdata.objects.all()
    return render(request, 'backend/contact_list.html', {'contacts': contacts})



def view_contact(request, id):
    contact = get_object_or_404(Contact_fromdata, id=id)
    contact_data = {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone_number": contact.phone_number,
        "message": contact.message,
        "address": contact.address,
        "created_at": contact.created_at,
    }
    return JsonResponse({"status": "success", "contact": contact_data})



@csrf_exempt
def delete_contact(request, id):
    contact = get_object_or_404(Contact_fromdata, id=id)

    if request.method == "POST":
        contact.delete()
        return JsonResponse({"status": "success", "message": "Contact deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BussinessBanner  # Import your BussinessBanner model

def sister_concern_banner_form(request):
    # Check if there is an existing banner or if it's a new form
    try:
        banner = BussinessBanner.objects.first()  # Get the first banner (or None if no banner exists)
    except BussinessBanner.DoesNotExist:
        banner = None
    
    if request.method == 'POST':
        # Title is optional since it has a default value, but you can allow users to update it.
        title = request.POST.get('title', '').strip() or "Bussiness"
        background_image = request.FILES.get('background_image')

        # Validate that a background image is provided
        if not background_image and not banner:
            messages.error(request, "Please upload a background image.")
            return redirect('add_sister_concern_banner')  # Replace with your URL name

        try:
            if banner:
                # Update existing banner if it exists
                banner.title = title
                if background_image:
                    banner.background_image = background_image
            else:
                # Create new banner if none exists
                banner = BussinessBanner(
                    title=title,
                    background_image=background_image
                )
            banner.save()

            messages.success(request, "Sister Concern Banner saved successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('sister_concern_banner_form')  # Change this to your desired URL

    # Pass the banner object to the template if it exists
    return render(request, 'backend/sisterConcern_banner_form.html', {'banner': banner})




def sister_concern_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        # image = request.FILES.get("image")
        # icon = request.FILES.get("icon")
        link = request.POST.get("link")

        sister_concern = SisterConcern(
            title=title, 
            description=description, 
            # image=image, 
            # icon=icon, 
            link=link
        )
        sister_concern.save()
        messages.success(request, "Sister Concern created successfully.")
        return redirect("sister_concern_list")  # Change as per your URL pattern

    return render(request, "backend/sister_concern_add.html")




def sister_concern_list(request):
    sister_concerns = SisterConcern.objects.all()
    return render(request, "backend/sister_concern_list.html", {"sister_concerns": sister_concerns})



def edit_sister_concern(request, id):
    concern = get_object_or_404(SisterConcern, id=id)

    if request.method == "POST":
        concern.title = request.POST.get("title")
        concern.description = request.POST.get("description")
        concern.link = request.POST.get("link")

        # if "image" in request.FILES:
        #     concern.image = request.FILES["image"]
        # if "icon" in request.FILES:
        #     concern.icon = request.FILES["icon"]

        concern.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})




def delete_sister_concern(request, id):
    if request.method == "POST":
        concern = get_object_or_404(SisterConcern, id=id)
        concern.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']
        filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"  # Unique filename
        file_path = os.path.join('uploads', filename)

        # Save the file in the media folder
        default_storage.save(os.path.join(settings.MEDIA_ROOT, file_path), ContentFile(uploaded_file.read()))

        # ✅ CKEditor expects the URL inside {"url": "your_image_url"}
        return JsonResponse({
            "uploaded": True,
            "url": f"{settings.MEDIA_URL}{file_path}"
        })

    return JsonResponse({'uploaded': False, 'error': {'message': 'Invalid request'}}, status=400)



def manage_videos(request):
    videos = Video.objects.all()

    if request.method == "POST":
        video_id = request.POST.get("video_id")
        title = request.POST.get("title")
        url = request.POST.get("url")

        if video_id:
            # Edit existing video
            video = get_object_or_404(Video, id=video_id)
            video.title = title
            video.url = url
            messages.success(request, "Video updated successfully!")
        else:
            # Add new video
            video = Video(title=title, url=url)
            messages.success(request, "Video added successfully!")

        video.save()
        return redirect("manage_videos")

    return render(request, "backend/manage_videos.html", {"videos": videos})

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    messages.success(request, "Video deleted successfully!")
    return redirect("manage_videos")