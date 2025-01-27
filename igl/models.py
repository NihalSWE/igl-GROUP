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
class Contact_ShedulSection(models.Model):
    title = models.CharField(max_length=255, default="Call or visit us at one of our different locations.")
    description = models.TextField(default="Amet minim mollit non deserunt ullamco est aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit amet minim mollit on.")
    button_text = models.CharField(max_length=100, default="Schedule a call")
    button_url = models.URLField(default="#",null=True,blank=True)

    def __str__(self):
        return self.title

#Location
class Contact_LocationSection(models.Model):
    section = models.ForeignKey(Contact_ShedulSection, related_name="locations", on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    phone_number = models.CharField(max_length=20)
    map_url = models.URLField(default="#",null=True,blank=True)
    image = models.ImageField(upload_to="locations/")

    def __str__(self):
        return self.city_name

