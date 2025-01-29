from django.shortcuts import render, redirect, get_object_or_404
from .models import CoverSection,ContactBanner,Contact_Schedule,Contact_Location, Contact_fromdata,Gallery,GalleryBanner,Blog,JobPosting, JobApplication
from django.http import JsonResponse



# Create your views here.

def base(request):
    return render(request, 'frontend/base.html')

def home(request):
    cover_section = CoverSection.objects.first()  # Fetch the first cover section
    return render(request, 'frontend/home.html', {'cover_section': cover_section})


def about(request):
    return render(request, 'frontend/about.html')

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


def gallery(request):
    banner = GalleryBanner.objects.first()
    photos = Gallery.objects.all().order_by('-uploaded_at')  # Order by most recent
    context = {
        'banner':banner,
        'photos': photos,
    }
    return render(request, 'frontend/gallery.html', context)

def case_studies(request):
    return render(request, 'frontend/case-studies.html')

def igl_web(request):
    return render(request, 'frontend/igl_web.html')

def bod(request):
    return render(request, 'frontend/BOD.html')

def bos(request):
    return render(request, 'frontend/BOS.html')

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


