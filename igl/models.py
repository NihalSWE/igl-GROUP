# models.py
from django.db import models
from PIL import Image, ImageOps

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
class CoverSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    button_text = models.CharField(max_length=100)
    url = models.CharField(max_length=255)  # Use CharField instead of URLField
    background_image = models.ImageField(upload_to='cover_section_images/')
    
    def __str__(self):
        return self.title
    
    
    
#------------Contact Page Model--------------

#banner
class ContactBanner(models.Model):
    title = models.CharField(max_length=255, default="Contact Us")
    background_image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title



#shedul
from django.db import models

class Contact_Schedule(models.Model):
    """
    Manages the main schedule/contact section's heading, description, and call-to-action button.
    """
    title = models.CharField(max_length=255, help_text="Main heading text for the contact section.")
    description = models.TextField(max_length=255,help_text="Short description or introduction.")
    button_text = models.CharField(max_length=100, help_text="Text for the call-to-action button.")
    button_link = models.URLField(help_text="URL the button redirects to.", blank=True, null=True)

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
    email = models.EmailField()
    message = models.TextField()
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

class Gallery(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)  # Optional title for the image
    image = models.ImageField(upload_to='gallery/')  # Uploads images to the 'gallery/' directory
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Tracks upload date

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first

        # Desired square size
        square_size = 500

        # Open the uploaded image
        img = Image.open(self.image.path)

        # Convert to RGB if the image has an alpha channel
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Create a square canvas with a white background
        img = ImageOps.fit(img, (square_size, square_size), Image.Resampling.LANCZOS, centering=(0.5, 0.5))

        # Save the resized image back to the same path
        img.save(self.image.path)
        
        
#--------blog model--------
from django.utils.text import Truncator
from ckeditor.fields import RichTextField

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()  # ✅ Use CKEditor for content
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Limit title to first 10 characters, adding '...' if too long
    def short_title(self):
        return Truncator(self.title).chars(10, truncate='...')

    # Get a snippet of the content with full words
    def snippet(self):
        return Truncator(self.content).words(15, truncate='...')

    # Resize image to a fixed size when saved
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img_path = self.image.path
            with Image.open(img_path) as img:
                img = img.resize((600, 400), Image.Resampling.LANCZOS)
                img.save(img_path)
                
                
                
                
#-----------career model-----

from django.urls import reverse

class JobPosting(models.Model):
    LOCATION_CHOICES = [
        ('dhaka', 'Dhaka'),
        ('chittagong', 'Chittagong'),
    ]

    title = models.CharField(max_length=200)
    short_description = RichTextField(max_length=200)
    full_description = RichTextField(max_length=5000)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)  # Kept as CharField
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
    location = models.CharField(max_length=100, editable=False, default='dhaka')  # Auto-filled from job
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='cvs/')
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically set the location from the job posting."""
        if self.job:
            self.location = self.job.location  # Auto-assign job's location
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.job.title} ({self.get_location_display()})"

    def get_location_display(self):
        """Convert location code to human-readable form."""
        location_dict = dict(JobPosting.LOCATION_CHOICES)
        return location_dict.get(self.location, self.location)