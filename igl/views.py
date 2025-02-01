from django.shortcuts import render, redirect, get_object_or_404
from .models import CoverSection,ContactBanner,Contact_Schedule,Contact_Location, Contact_fromdata, Gallery_Album, Gallery_AlbumDetails,GalleryBanner,Blog,JobPosting, JobApplication,BusinessStrength,BOD, Staff
from django.http import JsonResponse



# Create your views here.

def base(request):
    return render(request, 'frontend/base.html')

def home(request):
    cover_section = CoverSection.objects.first()  # Fetch the first cover section
    business_strengths = BusinessStrength.objects.all()
    blogs = Blog.objects.all().order_by('-published_date')[:3]
    industries = [
        {'name': 'Publishing', 'icon': 'line-icon-Microphone-4', 'link': '#'},
        {'name': 'Finance', 'icon': 'line-icon-Basket-Coins', 'link': '#'},
        {'name': 'Sciences', 'icon': 'line-icon-Bee', 'link': '#'},
        {'name': 'Consultant', 'icon': 'line-icon-Management', 'link': '#'},
        {'name': 'Food', 'icon': 'line-icon-French-Fries', 'link': '#'},
        {'name': 'Travel', 'icon': 'line-icon-Road-3', 'link': '#'},
        {'name': 'Dairy', 'icon': 'line-icon-Cow', 'link': '#'},
        {'name': 'Jewellery', 'icon': 'line-icon-Diamond', 'link': '#'},
        {'name': 'Energy', 'icon': 'line-icon-Drop', 'link': '#'},
        {'name': 'Farming', 'icon': 'line-icon-Environmental-3', 'link': '#'},
        {'name': 'Industries', 'icon': 'line-icon-Gear', 'link': '#'},
        {'name': 'Events', 'icon': 'line-icon-Environmental-3', 'link': '#'}
    ]
    context={
        'cover_section': cover_section,
        'business_strengths': business_strengths,
        'industries': industries,
        'blogs': blogs,
    }
    return render(request, 'frontend/home.html', context)


def about(request):
    # bod_members = BOD.objects.all()
    staff_members = Staff.objects.all()
    context = {
        # 'bod_members': bod_members,
        'staff_members': staff_members,
        }
    return render(request, 'frontend/about.html',context)

def contact(request):
    # Fetch the necessary data for rendering the page
    banner = ContactBanner.objects.first()
    contact_schedule = Contact_Schedule.objects.first()
    contact_locations = Contact_Location.objects.all()

    if request.method == 'POST':
        # Get the form data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('comment')

        # Save the data to the database
        contact_form_data = Contact_fromdata(name=name, email=email, message=message)
        contact_form_data.save()

        # Return the success message as a JSON response to update the page asynchronously
        return JsonResponse({"success_message": "Your message has been successfully sent. We will get back to you shortly!"})

    # Render the form with necessary context (for GET request)
    context = {
        "banner": banner,
        "contact_schedule": contact_schedule,
        "contact_locations": contact_locations,
    }

    return render(request, 'frontend/contact.html', context)


# In views.py
def gallery(request):
    banner = GalleryBanner.objects.first()  # Fetch the banner
    albums = Gallery_Album.objects.all().order_by('-created_at')  # Fetch all albums, ordered by creation date
    context = {
        'banner': banner,
        'albums': albums,  # Pass the albums to the template
    }
    return render(request, 'frontend/gallery.html', context)

def album_images(request, album_id):
    banner = GalleryBanner.objects.first()  # Fetch the banner
    album = get_object_or_404(Gallery_Album, id=album_id)  # Get the album based on the clicked album's ID
    images = Gallery_AlbumDetails.objects.filter(album=album).order_by('-uploaded_at')  # Fetch all images for this album
    
    context = {
        'banner': banner,
        'album': album,
        'images': images,  # Pass the images of the selected album
    }
    return render(request, 'frontend/gallery_single.html', context)


def Bussiness(request):
    business_strengths = BusinessStrength.objects.all()
    context = {
        'business_strengths': business_strengths,
    }
    return render(request, 'frontend/bussiness.html',context)

def igl_web(request):
    return render(request, 'frontend/igl_web.html')

def bod(request):
    bod_members = BOD.objects.all()
    context = {
        'bod_members': bod_members,
        }
    return render(request, 'frontend/BOD.html',context)

def bos(request):
    staff_members = Staff.objects.all()
    context = {
        'staff_members': staff_members,
        }
    return render(request, 'frontend/BOS.html',context)

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import JobPosting, JobApplication

# Career page
def career(request):
   # Get all jobs
    all_jobs = JobPosting.objects.filter(is_active=True).order_by('-posted_date')
    # Filter Dhaka jobs
    dhaka_jobs = all_jobs.filter(location='dhaka')
    # Filter Chittagong jobs
    chittagong_jobs = all_jobs.filter(location='chittagong')

    return render(request, 'frontend/career.html', {
        'jobs': all_jobs,
        'dhaka_jobs': dhaka_jobs,
        'chittagong_jobs': chittagong_jobs,
    })

# Job Detail page
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    return render(request, 'frontend/job_details.html', {'job': job})

# Submit application view
def submit_application(request, job_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        linkedin_url = request.POST.get('linkedin', '')
        portfolio_url = request.POST.get('portfolio', '')
        cv = request.FILES.get('cv')
        
        # Validate required fields
        if not name or not email or not phone or not cv:
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})
        
        job = get_object_or_404(JobPosting, id=job_id)

        # Create and save the job application
        application = JobApplication(
            job=job,
            name=name,
            email=email,
            phone=phone,
            cv=cv,
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url
        )
        application.save()

        messages.success(request, 'Your application has been submitted successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})





def blog(request):
    blogs = Blog.objects.all().order_by('-published_date')
    context = {
        'blogs': blogs,
    }
    return render(request, 'frontend/blogs.html', context)

def blog_single(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        'blog': blog,
    }
    return render(request, 'frontend/blog-single.html', context)


