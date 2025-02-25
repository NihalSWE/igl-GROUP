from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse



# Create your views here.

def base(request):
    return render(request, 'frontend/base.html')


# def footer_view(request):
#     # Get only the 'title' and 'link' fields from SisterConcern
#     sister_concerns = SisterConcern.objects.values('title', 'link')

#     # Split the concerns into two columns
#     column1 = sister_concerns[::2]  # Get items for column 1 (odd index)
#     column2 = sister_concerns[1::2]  # Get items for column 2 (even index)

#     return render(request, 'your_template_name.html', {'column1': column1, 'column2': column2})

def home(request):
    intro = HomeIntro.objects.last()
    cover_section = HomeBanner.objects.first()
    
    industries = Industry.objects.all()
    banner = ContactBanner.objects.first()
    reasons = ReasonToChooseUs.objects.all()
   
    contact_image = ContactBanner.objects.first()

    context = {
        'intro': intro,
        'cover_section': cover_section,
        
       
        'contact_image': contact_image,
        'industries': industries,
        "banner": banner,
        "reasons": reasons,
        "banner_images": cover_section.images.all() if cover_section else [],
    }
    return render(request, 'frontend/home.html', context)



def about(request):
    banner = AboutBanner.objects.first()
    about_section=AboutSection.objects.first()
   
    context = {
        "banner": banner,
        "about_section":about_section,
        
        }
    return render(request, 'frontend/about.html',context)

def contact(request):
    return render(request, 'frontend/contact.html')

def address(request):
    banner = ContactBanner.objects.first()
    contact_schedule = Contact_Schedule.objects.first()
    contact_locations = Contact_Location.objects.all()
    context = {
        "banner": banner,
        "contact_schedule": contact_schedule,
        "contact_locations": contact_locations,
    }
    return render(request, 'frontend/Address.html', context)

def feedback(request):
    banner = ContactBanner.objects.first()
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the form data, including new fields
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone_number = request.POST.get('phone_number')  # Get phone number
        address = request.POST.get('address')  # Get address

        # Save the feedback data to the database
        feedback_data = Contact_fromdata(
            name=name,
            email=email,
            message=message,
            phone_number=phone_number,  # Save phone number
            address=address  # Save address
        )
        feedback_data.save()

        # Return the success message as a JSON response for asynchronous page update
        return JsonResponse({"success_message": "Thank you for your feedback! We will review it shortly."})

    context = {
        "banner": banner,
    }
    return render(request, 'frontend/Feedback.html', context)

def location_map(request):
    banner = ContactBanner.objects.first()
    context = {
        "banner": banner,
    }
    return render(request, 'frontend/location_Map.html', context)


# In views.py
def gallery(request):
    banner = GalleryBanner.objects.first()  # Fetch the banner
    albums = Gallery_Album.objects.all().order_by('-created_at')  # Fetch all albums, ordered by creation date
    context = {
        'banner': banner,
        'albums': albums,  # Pass the albums to the template
    }
    return render(request, 'frontend/gallery.html', context)

def album_images(request, album_slug):
    banner = GalleryBanner.objects.first()  # Fetch the banner
    album = get_object_or_404(Gallery_Album, slug=album_slug)  # Get the album based on the slug
    images = Gallery_AlbumDetails.objects.filter(album=album).order_by('-uploaded_at')  # Fetch all images for this album
    
    context = {
        'banner': banner,
        'album': album,
        'images': images,  # Pass the images of the selected album
    }
    return render(request, 'frontend/gallery_single.html', context)

from django.core.paginator import Paginator
def vdo_gly(request):
    banner = GalleryBanner.objects.first()  # Fetch the banner
    videos_list = Video.objects.all().order_by('-created_at')  # Fetch all videos
    paginator = Paginator(videos_list, 15)  # 15 videos per page

    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)  # Get videos for the current page

    context = {
        'banner': banner,
        'videos': videos,  # This is now a paginated object
    }
    return render(request, 'frontend/video_gallery.html', context)


def Bussiness(request):
    banner = BussinessBanner.objects.first()  # Fetch the banner
 
    context = {
        'banner': banner,
        
    }
    return render(request, 'frontend/bussiness.html',context)



def bod(request):
    banner = OurTeamBanner.objects.first()
    bod_members = BOD.objects.all()
    context = {
        'banner': banner,
        'bod_members': bod_members,
    }
    return render(request, 'frontend/BOD.html', context)


def bod_single(request, slug):
    banner = OurTeamBanner.objects.first()
    member = get_object_or_404(BOD, slug=slug)  # Using name to get the member
    context = {
        'banner': banner,
        'member': member,
    }
    return render(request, 'frontend/BOD_Single.html', context)

def bos(request):
    banner = OurTeamBanner.objects.first()
    staff_members = Staff.objects.all()
    context = {
        'banner': banner,
        'staff_members': staff_members,
        }
    return render(request, 'frontend/BOS.html',context)

def bos_single(request, slug):
    banner = OurTeamBanner.objects.first()
    member = get_object_or_404(Staff, slug=slug)  # Using name to get the member
    context = {
        'banner': banner,
        'member': member,
    }
    return render(request, 'frontend/BOS_Single.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import JobPosting, JobApplication

# Career page
def career(request):
    banner=CareerBanner.objects.first()
    images = CareerImages.objects.filter(is_active=True).last()
   # Get all jobs
    all_jobs = JobPosting.objects.filter(is_active=True).order_by('-posted_date')
    

    return render(request, 'frontend/career.html', {
        'banner': banner,
        'images': images,
        'jobs': all_jobs,
        
    })

# Job Detail page
def job_detail(request, pk):
    banner=CareerBanner.objects.first()
    job = get_object_or_404(JobPosting, pk=pk)
    
    return render(request, 'frontend/job_details.html', {'job': job,'banner': banner,})

# Submit application view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import JobPosting, JobApplication

from django.utils.timezone import now


def submit_application(request, job_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender', 'male')  # Default to 'male'
        linkedin_url = request.POST.get('linkedin', '')
        portfolio_url = request.POST.get('portfolio', '')
        cv = request.FILES.get('cv')
        image = request.FILES.get('image', None)  # Image upload support

        # Validate required fields
        if not name or not email or not phone or not cv:
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})

        job = get_object_or_404(JobPosting, id=job_id)
        
        # Check if user has already applied for this job before the deadline
        existing_application = JobApplication.objects.filter(job=job, phone=phone).first()
        if existing_application and job.deadline >= now().date():
            return JsonResponse({'status': 'error', 'message': 'You have already applied for this job. You can reapply after the deadline.'})

        # Create and save the job application
        application = JobApplication(
            job=job,
            location=job.location,  # Auto-fill location
            department=job.department,  # Auto-fill department
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            cv=cv,
            image=image,  # Save uploaded image
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url
        )
        application.save()

        messages.success(request, 'Your application has been submitted successfully!')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def check_application(request):
    phone = request.GET.get('phone')

    if phone:
        # Check if the phone number exists in the database
        application = JobApplication.objects.filter(phone=phone).first()

        if application:
            # Return the existing application data
            data = {
                'exists': True,
                'name': application.name,
                'email': application.email,
                'gender': application.gender,
                'linkedin_url': application.linkedin_url,
                'portfolio_url': application.portfolio_url
            }
        else:
            # No application found for the phone number
            data = {'exists': False}
        
        return JsonResponse(data)

    return JsonResponse({'status': 'error', 'message': 'Phone number is required.'})







# def blog(request):
#     banner=BlogBanner.objects.first()
#     blogs = Blog.objects.all().order_by('-published_date')
#     context = {
#         'banner': banner,
#         'blogs': blogs,
#     }
#     return render(request, 'frontend/blogs.html', context)

# def blog_single(request, pk):
#     banner=BlogBanner.objects.first()
#     blog = get_object_or_404(Blog, pk=pk)
#     context = {
#         'banner': banner,
#         'blog': blog,
#     }
#     return render(request, 'frontend/blog-single.html', context)



# def igl_web(request):
#     igl_web_data = IGL_WEB.objects.all()
#     banner = BussinessBanner.objects.first()  # Fetch the banner
#     context={
#         'igl_webs': igl_web_data,
#         'banner': banner,
#     }
#     return render(request, 'frontend/igl_web.html', context)

# def igl_host(request):
#     igl_host_data = IGL_HOST.objects.all()
#     banner = BussinessBanner.objects.first()  # Fetch the banner
#     context={
#         'igl_hosts': igl_host_data,
#         'banner': banner,
#     }
#     return render(request, 'frontend/igl_host.html', context)

# def stdnt_visa(request):
#     student_visa_data = STUDENT_VISA.objects.all()
#     banner = BussinessBanner.objects.first()  # Fetch the banner
#     context={
#         'student_visas': student_visa_data,
#         'banner': banner,
#     }
#     return render(request, 'frontend/studentvisa.html', context)

# def felnatech(request):
#     felnatech_data = FELNA_TECH.objects.all()
#     banner = BussinessBanner.objects.first()  # Fetch the banner
#     context={
#         'felnatechs': felnatech_data,
#         'banner': banner,
#     }
#     return render(request, 'frontend/felnatech.html', context)


def sister_concern_single(request, slug):
    sister_concern = SisterConcern.objects.filter(slug=slug).first()  # Use slug instead of id
    if not sister_concern:
        return redirect("sister_concern_list")  # Redirect if not found (optional)

    banner = BussinessBanner.objects.first()

    context = {
        "sister_concern": sister_concern,
        "banner": banner,
        "title": sister_concern.title,  # Use the title directly
    }
    return render(request, "frontend/sister_concern_single.html", context)







def our_customer(request):
    banner = ContactBanner.objects.first()
    industries = Industry.objects.all()
    context={
        'banner': banner,
        'industries': industries,
        
    }
    return render (request,'frontend/our_customers.html', context)


def policy(request):
    cover_section = HomeBanner.objects.first()
    context={
        'cover_section': cover_section,
    }
    return render(request,'frontend/policy.html',context)

def terms(request):
    cover_section = HomeBanner.objects.first()
    context={
        'cover_section': cover_section,
    }
    return render(request,'frontend/terms.html',context)


def error_page(request, exception):
    return render(request, 'frontend/404.html')




