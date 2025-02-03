# admin.py
from django.contrib import admin
from .models import NavMenu, Logo,HomeIntro,HomeBanner,AboutBanner,ContactBanner,CareerBanner,BussinessBanner,BlogBanner,Contact_Schedule, Contact_Location,Contact_fromdata,Gallery_AlbumDetails,Gallery_Album,GalleryBanner,Blog,BusinessStrength,AboutSection,ClientReview,Industry,ReasonToChooseUs


@admin.register(NavMenu)
class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent', 'is_active']
    list_filter = ['parent']
    search_fields = ['name']

#----------home page----

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['id','image', 'is_active']
    

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'button_text']
    
@admin.register(HomeIntro)
class HomeIntroAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'progress1_title', 'progress2_title']

@admin.register(Industry)   
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'link')
    search_fields = ('name', 'icon')

@admin.register(ReasonToChooseUs)
class ReasonToChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)

#------About us--------
@admin.register(AboutBanner)
class AboutBannerAdmin(admin.ModelAdmin):
    list_display = ['title']
    
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'text','created_at')
    
    
#-----contact page----

@admin.register(ContactBanner)
class ContactBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    

@admin.register(Contact_Schedule)
class ContactScheduleAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text", "button_link")
    search_fields = ("title", "description")


@admin.register(Contact_Location)
class ContactLocationAdmin(admin.ModelAdmin):
    list_display = ("city", "address", "phone_number")
    search_fields = ("city", "address", "phone_number")


@admin.register(Contact_fromdata)
class ContactFromdataAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")


#-----------gallery page----
@admin.register(GalleryBanner)
class GalleryBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)

from .models import Gallery_Album, Gallery_AlbumDetails

class Gallery_AlbumDetailsInline(admin.TabularInline):
    model = Gallery_AlbumDetails  # Use Gallery_AlbumDetails for inlines
    extra = 1  # You can adjust the number of empty forms shown

@admin.register(Gallery_Album)
class Gallery_AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'thumbnail')  # Fields to display in the list view
    search_fields = ('title',)  # Enable search for album titles
    inlines = [Gallery_AlbumDetailsInline]  # Inline Gallery images inside Album admin

@admin.register(Gallery_AlbumDetails)
class Gallery_AlbumDetailsAdmin(admin.ModelAdmin):
    list_display = ('album', 'image', 'uploaded_at')  # Display album and image
    ordering = ('-uploaded_at',)  # Order gallery images by uploaded date, latest first
    search_fields = ('album__title',)  # Enable search for images by album title
    
#--------------blog--------
from django.db import models  # ✅ Import models
from ckeditor.widgets import CKEditorWidget

@admin.register(BlogBanner)
class BlogBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    
#-----------career----------
from .models import JobPosting, JobApplication

@admin.register(CareerBanner)
class CareerBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'posted_date', 'deadline', 'is_active','salary')
    list_filter = ('job_type', 'is_active', 'location')
    search_fields = ('title', 'description')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'location', 'applied_date')
    list_filter = ('job', 'applied_date')
    search_fields = ('name', 'email', 'phone')
    
    
    
#-----Bussiness--------
@admin.register(BussinessBanner)
class BussinessBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(BusinessStrength)
class BusinessStrengthAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'icon', 'link']
    
    
#----------Our Team---
from .models import BOD, Staff

@admin.register(BOD)
class BODAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name',)
