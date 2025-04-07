# models.py
from django.db import models
from PIL import Image, ImageOps
from ckeditor.fields import RichTextField
# Model for Navigation Menu

class NavMenu(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)  # Use CharField instead of URLField
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_menus')

    def __str__(self):
        return self.name


# Model for Logo
class Logo(models.Model):
    image = models.ImageField(upload_to='logos/')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Resize the logo before saving if it's too large
        if self.image:
            img = Image.open(self.image)
            img.thumbnail((200, 200))  # Resize to 200x200 max dimensions
            img.save(self.image.path)  # Save the image back to the original path
        super().save(*args, **kwargs)

    def __str__(self):
        return "Logo"

#------------Home Page Model--------------
#CoverSecton (Banner,Title,Description,Button link)
class HomeBanner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    button_text = models.CharField(max_length=100)
    url = models.CharField(max_length=255)  # Keep as CharField
    background_image = models.ImageField(upload_to='cover_section_images/')  # Keep for fallback

    def __str__(self):
        return self.title


class HomeBannerImage(models.Model):
    banner = models.ForeignKey(HomeBanner, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cover_section_images/')

    def __str__(self):
        return f"Image for {self.banner.title}"

    

#home intro
class HomeIntro(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField() 
    image1 = models.ImageField(upload_to="home_intro/")
   
    progress1_title = models.CharField(max_length=255)
    progress1_value = models.IntegerField()
    progress2_title = models.CharField(max_length=255)
    progress2_value = models.IntegerField()

    def __str__(self):
        return self.title
    
    
#INdustry links
class Industry(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='uploads/industry_icons/', blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

#reson to choose
from django.db import models
from ckeditor.fields import RichTextField
class ReasonToChooseUs(models.Model):
    ICON_CHOICES = [
        ("🎯", "Target (🎯)"),
        ("✉️", "Envelope (✉️)"),
        ("🚀", "Rocket (🚀)"),
        ("💡", "Lightbulb (💡)"),
        ("📈", "Chart Growth (📈)"),
        ("⚙️", "Gear (⚙️)"),
        ("🔗", "Link (🔗)"),
        ("🎨", "Palette (🎨)"),
        ("🔍", "Magnifying Glass (🔍)"),
        ("🛡️", "Shield (🛡️)"),
        ("🏆", "Trophy (🏆)"),
        ("🤝", "Handshake (🤝)"),
        ("💎", "Diamond (💎)"),
        ("📌", "Push Pin (📌)"),
        ("🔬", "Microscope (🔬)"),
    ]

    title = models.CharField(max_length=255)
    description =RichTextField(max_length=500)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default="🎯")
    order = models.PositiveIntegerField(default=0, help_text="Determines the order of display")

    class Meta:
        ordering = ["order"]  # Ensures the correct order is maintained

    def __str__(self):
        return self.title


#------------About Page Model--------------
#banner
class AboutBanner(models.Model):
    title = models.CharField(max_length=255, default="About Us")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title
    
#AboutSection
from io import BytesIO
from django.core.files.base import ContentFile
class AboutSection(models.Model):
    image = models.ImageField(upload_to="about_section/",default="No Image Uploaded",null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        """Resize image to 640px width while maintaining aspect ratio before saving."""
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()

            # Define the target width
            target_width = 600
            aspect_ratio = img.height / img.width
            target_height = int(target_width * aspect_ratio)  # Maintain aspect ratio

            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)  # ✅ Fixed this line
            img.save(output, format='JPEG', quality=90)  # Save resized image with good quality
            output.seek(0)

            # Save resized image back to the model
            self.image = ContentFile(output.read(), self.image.name)

        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"About Section - {self.id}"  # Unique identifier
    
#Client review
# class ClientReview(models.Model):
#     name = models.CharField(max_length=255)
#     company = models.CharField(max_length=255)
#     text = models.TextField(max_length=255)
#     image = models.ImageField(upload_to='client_reviews/')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.company}"
    
#------------Contact Page Model--------------

#banner
class ContactBanner(models.Model):
    title = models.CharField(max_length=255, default="Contact Us")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title



#shedul
class Contact_Schedule(models.Model):
    """
    Manages the main schedule/contact section's heading, description, and call-to-action button.
    """
    title = models.CharField(max_length=255, help_text="Main heading text for the contact section.")
    description = models.TextField(max_length=255,help_text="Short description or introduction.")
    button_text = models.CharField(max_length=100, help_text="Text for the call-to-action button.")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number.")  # New Field

    def __str__(self):
        return self.title

#location
class Contact_Location(models.Model):
    """
    Manages the details of individual locations, including an embedded Google Maps iframe.
    """
    city = models.CharField(max_length=100, help_text="City name.")
    address = models.TextField(max_length=255,help_text="Full address of the location.")
    map_url = models.URLField(
        help_text="Google Maps link for the location. Paste the link from Google Maps.",
        blank=True,
        null=True
    )
    phone_number = models.CharField(max_length=20, help_text="Phone number for the location.")
    TNT_number=models.CharField(max_length=20,null=True,blank=True, help_text="TNT number for the location.")
    
    image = models.ImageField(upload_to="locations/", help_text="Image or background for the location.")

    def resize_image(self):
        """
        Resize image to a standard size (e.g., 300x200px).
        """
        img = Image.open(self.image)
        img = img.resize((300, 200), Image.Resampling.LANCZOS)  # Using LANCZOS for high-quality resizing
        
        # Save the image back to the same path
        img.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        Overriding the save method to resize the image before saving it.
        """
        if self.image:
            self.resize_image()
        super(Contact_Location, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.city} - {self.address}"
    
    
#From Data

class Contact_fromdata(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # New phone number field
    address = models.TextField(blank=True, null=True)  # New address field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
    
    
#-----------Gallery page model-------
#banner
class GalleryBanner(models.Model):
    title = models.CharField(max_length=255, default="Contact Us")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title

from PIL import Image, ImageOps

from django.utils.text import slugify

class Gallery_Album(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)  # Album name
    thumbnail = models.ImageField(upload_to='albums/thumbnails/', blank=True, null=True)  # Thumbnail for the album
    created_at = models.DateTimeField(auto_now_add=True)  # Tracks album creation date
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug field

    def __str__(self):
        return self.title if self.title else f"Gallery_Album {self.id}"

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if self.thumbnail:
            # Resize the thumbnail to 300x300
            img = Image.open(self.thumbnail.path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img.save(self.thumbnail.path)  # Save the resized thumbnail

        

class Gallery_AlbumDetails(models.Model):
    album = models.ForeignKey(Gallery_Album, related_name='images', on_delete=models.CASCADE)  # Associate each image with an album
    image = models.ImageField(upload_to='gallery/')  # Image field
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Tracks upload date

    def __str__(self):
        return self.album.title if self.album and self.album.title else f"Image {self.id}"

    def save(self, *args, **kwargs):
        # First save the instance
        super().save(*args, **kwargs)

        if self.image:
            # Resize the image to 600x400
            img = Image.open(self.image.path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((600, 400), Image.Resampling.LANCZOS)
            img.save(self.image.path)  # Save the resized image
  


#--------------video gallery model-------------------
import re

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(help_text="Enter the YouTube or Vimeo URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def embed_url(self):
        """
        Converts a YouTube or Vimeo URL into an embeddable format.
        """
        youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]+)"
        vimeo_pattern = r"(?:https?:\/\/)?(?:www\.)?vimeo\.com\/(\d+)"

        youtube_match = re.search(youtube_pattern, self.url)
        vimeo_match = re.search(vimeo_pattern, self.url)

        if youtube_match:
            return f"https://www.youtube.com/embed/{youtube_match.group(1)}"
        elif vimeo_match:
            return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"
        else:
            return self.url  # Return as is if no match
      
        
#--------blog model--------
# from django.utils.text import Truncator
# from ckeditor.fields import RichTextField

# #banner
# class BlogBanner(models.Model):
#     title = models.CharField(max_length=255, default="Blog")
#     background_image = models.ImageField(upload_to='banners/')
    
#     def __str__(self):
#         return self.title

# #blog
# class Blog(models.Model):
#     title = models.CharField(max_length=255)
#     content = RichTextField()  # ✅ Use CKEditor for content
#     image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
#     published_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     # Limit title to first 10 characters, adding '...' if too long
#     def short_title(self):
#         return Truncator(self.title).chars(10, truncate='...')

#     # Get a snippet of the content with full words
#     def snippet(self):
#         return Truncator(self.content).words(15, truncate='...')

#     # Resize image to a fixed size when saved
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.image:
#             img_path = self.image.path
#             with Image.open(img_path) as img:
#                 img = img.resize((600, 400), Image.Resampling.LANCZOS)
#                 img.save(img_path)
                
                
                
                
#-----------career model-----
#banner
class CareerBanner(models.Model):
    title = models.CharField(max_length=255, default="Career")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title


#career page images 
class CareerImages(models.Model):
    main_image = models.ImageField(upload_to='career_images/', help_text="Large main image (800x600)")
    group_image = models.ImageField(upload_to='career_images/', help_text="Group image (400x300)")
    activity_image1 = models.ImageField(upload_to='career_images/', help_text="First activity image (300x200)")
    activity_image2 = models.ImageField(upload_to='career_images/', help_text="Second activity image (300x200)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Career Page Images"
        verbose_name_plural = "Career Page Images"

    def __str__(self):
        return f"Career Images Set - {self.created_at.strftime('%Y-%m-%d')}"


#job posting
from django.urls import reverse
class JobPosting(models.Model):
    LOCATION_CHOICES = [
        ('dhaka', 'Dhaka'),
        ('chittagong', 'Chittagong'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('SEO', 'SEO'),
        ('SOFTWARE', 'Software'),
        ('TELESALES', 'Telesales'),
        ('HR', 'HR'),
        ('ACCOUNTS', 'Accounts'),
    ]

    title = models.CharField(max_length=200)
    short_description = RichTextField(max_length=200)
    full_description = RichTextField(max_length=5000)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default="dhaka")  
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default="IT")  # Department field
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
        ]
    )
    salary = models.CharField(max_length=100, null=True, help_text="Specify salary range (e.g., 30,000 - 50,000 BDT)")
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.get_location_display()}"

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])



class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    location = models.CharField(max_length=100, editable=False, default='dhaka')  
    department = models.CharField(max_length=50, editable=False, default='IT')  # Auto-filled from job posting
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='Male')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='cvs/')
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)  # New field for Twitter
    portfolio_url = models.URLField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """Auto-fill location and department from the job posting."""
        if self.job:
            self.location = self.job.location  # Auto-assign job's location
            self.department = self.job.department  # Auto-assign job's department
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.job.title} ({self.get_location_display()})"

    def get_location_display(self):
        """Convert location code to human-readable form."""
        location_dict = dict(JobPosting.LOCATION_CHOICES)
        return location_dict.get(self.location, self.location)


    
    
    
#-----------Bussiness model------
#banner
class BussinessBanner(models.Model):
    title = models.CharField(max_length=255, default="Bussiness")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title

#websites
# class BusinessStrength(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(max_length=200)
#     image = models.ImageField(upload_to='business_strength/')
#     icon = models.ImageField(upload_to='business_strength/icons/')
#     link = models.URLField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)  # Save the original image first

#         # Set the standard size for the business/company image
#         standard_size = (800, 600)  # Fixed width x height

#         # Resize the main image
#         if self.image:
#             img = Image.open(self.image.path)
#             img = img.resize(standard_size)  # Resize image to fixed size
#             img.save(self.image.path)  # Save the resized image

#         # Resize the icon image to a smaller fixed size (optional)
#         if self.icon:
#             icon_size = (100, 100)  # Example: Fixed size for icons
#             icon = Image.open(self.icon.path)
#             icon = icon.resize(icon_size)  # Resize icon to fixed size
#             icon.save(self.icon.path)  # Save the resized icon
            
# New models that only use title, description, and image
class IGL_WEB(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(max_length=5000)
    image = models.ImageField(upload_to='igl_web/')
    def __str__(self):
        return self.title

class IGL_HOST(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(max_length=5000)
    image = models.ImageField(upload_to='igl_host/')
    def __str__(self):
        return self.title

class STUDENT_VISA(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(max_length=5000)
    image = models.ImageField(upload_to='student_visa/')
    def __str__(self):
        return self.title

class FELNA_TECH(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(max_length=5000)
    image = models.ImageField(upload_to='felna_tech/')
    def __str__(self):
        return self.title
    
            
#----------Our Team model-----
class OurTeamBanner(models.Model):
    title = models.CharField(max_length=255, default="Our Team")
    background_image = models.ImageField(upload_to='banners/')
#-----Director

from django.utils.text import slugify
class BOD(models.Model):
    name = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='bod_images/')
    bio = models.TextField(max_length=1000, blank=True, null=True)
    portfolio_link = models.URLField(max_length=500, blank=True, null=True)  # Portfolio link field
    pdf = models.FileField(upload_to='bod_pdfs/', blank=True, null=True)  # PDF field for file uploads
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug field for URL-friendly representation

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't already exist
            # Generate a slug from the name and replace hyphens with underscores
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)  # Save the BOD instance

        # Resize image if it exists
        if self.image and hasattr(self.image, 'path'):
            self.resize_image(self.image.path)

    def resize_image(self, image_path):
        """Resize the image to a standard size of 600x600."""
        with Image.open(image_path) as img:
            size = (600, 600)  # Standard square size
            img = img.resize(size, Image.LANCZOS)
            img.save(image_path)
    
    
#-----Staff
class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    bio = models.TextField(max_length=1000, blank=True, null=True)
    portfolio_link = models.URLField(max_length=500, blank=True, null=True,default="Not Uploaded")  # Portfolio link field
    pdf = models.FileField(upload_to='bod_pdfs/', blank=True, null=True,default="Not Uploaded")  # PDF field for file uploads
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug field for URL-friendly representation

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't already exist
            # Generate a slug from the name and replace hyphens with underscores
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)  # Save the BOD instance

        # Resize the image if it exists
        if self.image and hasattr(self.image, 'path'):
            image_path = self.image.path
            # Open and resize the image
            with Image.open(image_path) as img:
                size = (400, 400)  # Square dimensions
                img = img.resize(size, Image.LANCZOS)
                
                # Save the resized image
                img.save(image_path)
                
                
#websites
class SisterConcern(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # Slug field for SEO-friendly URLs
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='business_strength/')
    icon = models.ImageField(upload_to='business_strength/icons/')
    link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while SisterConcern.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)


        # Resize the main image if exists
        if self.image:
            img = Image.open(self.image.path)
            standard_size = (800, 600)  # Fixed width x height
            img = img.resize(standard_size)
            img.save(self.image.path)  # Save the resized image

        # Resize the icon if exists
        if self.icon:
            icon = Image.open(self.icon.path)
            icon_size = (100, 100)  # Fixed size for icons
            icon = icon.resize(icon_size)
            icon.save(self.icon.path)  # Save the resized icon
            
            
            
class WeServe(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='weserve_icons/')
    
    def __str__(self):
        return self.name