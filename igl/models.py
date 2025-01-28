# models.py
from django.db import models
from PIL import Image

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