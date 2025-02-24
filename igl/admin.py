# admin.py
from django.contrib import admin
from .models import NavMenu, Logo,HomeIntro,HomeBanner,HomeBannerImage,AboutBanner,ContactBanner,CareerBanner,BussinessBanner,Contact_Schedule, Contact_Location,Contact_fromdata,Gallery_AlbumDetails,Gallery_Album,GalleryBanner,IGL_WEB, IGL_HOST, STUDENT_VISA, FELNA_TECH,AboutSection,Industry,ReasonToChooseUs,CareerImages
# from jazmin.sites import AdminSite
# from django.urls import reverse
# from . models import get_admin_url
# from django.utils.translation import gettext_lazy as _



@admin.register(NavMenu)
class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent', 'is_active']
    list_filter = ['parent']
    search_fields = ['name']

#----------home page----

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['id','image', 'is_active']
    

class HomeBannerImageInline(admin.TabularInline):  # Allows inline editing
    model = HomeBannerImage
    extra = 1  # Allows adding extra images in admin

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'url')  # Fields to show in the list
    search_fields = ('title', 'description')  # Searchable fields
    inlines = [HomeBannerImageInline]  # Attach images as inline

@admin.register(HomeBannerImage)
class HomeBannerImageAdmin(admin.ModelAdmin):
    list_display = ('banner', 'image')  # Display image and its banner
    
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
    list_display = ('id','image')
    
# @admin.register(ClientReview)
# class ClientReviewAdmin(admin.ModelAdmin):
#     list_display = ('name', 'company', 'text','created_at')
    
    
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
     list_display = ("name", "email", "phone_number", "address", "message", "created_at")
     search_fields = ("name", "email", "phone_number", "address", "message")


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
    
    
#-------------video galley page ---

from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title',)    

#--------------blog--------
# from django.db import models  # ✅ Import models
# from ckeditor.widgets import CKEditorWidget

# @admin.register(BlogBanner)
# class BlogBannerAdmin(admin.ModelAdmin):
#     list_display = ('title',)


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'published_date')
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget()},
#     }
    
#-----------career----------
from .models import JobPosting, JobApplication
from django.utils.html import format_html

@admin.register(CareerBanner)
class CareerBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    
@admin.register(CareerImages)
class CareerImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'preview_main_image', 'preview_group_image', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('created_at',)

    def preview_main_image(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" height="75" style="border-radius:5px;"/>', obj.main_image.url)
        return "No Image"
    
    def preview_group_image(self, obj):
        if obj.group_image:
            return format_html('<img src="{}" width="100" height="75" style="border-radius:5px;"/>', obj.group_image.url)
        return "No Image"
    
    preview_main_image.short_description = "Main Image"
    preview_group_image.short_description = "Group Image"

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'department', 'job_type', 'salary', 'deadline', 'is_active')
    list_filter = ('location', 'department', 'job_type', 'is_active')
    search_fields = ('title', 'department', 'location')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'department', 'location', 'gender', 'image','applied_date','cv')
    list_filter = ('department', 'location', 'gender')
    search_fields = ('name', 'email', 'phone', 'job__title')
    
    
    
#-----Bussiness--------
@admin.register(BussinessBanner)
class BussinessBannerAdmin(admin.ModelAdmin):
    list_display = ('title',)

# @admin.register(BusinessStrength)
# class BusinessStrengthAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'image', 'icon', 'link']
    
@admin.register(IGL_WEB)
class IGLWEBAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image']
   

@admin.register(IGL_HOST)
class IGLHOSTAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image']
    

@admin.register(STUDENT_VISA)
class STUDENTVISAAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image']
    

@admin.register(FELNA_TECH)
class FELNATECHAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image']
   
#----------Our Team---
from .models import BOD, Staff,OurTeamBanner

@admin.register(OurTeamBanner)
class OurTeamBannerAdmin(admin.ModelAdmin):
    list_display = ('id','title','background_image')

@admin.register(BOD)
class BODAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'portfolio_link', 'pdf')  # Add the fields to display
    search_fields = ('name', 'role')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'portfolio_link', 'pdf')
    search_fields = ('name',)


# class CustomAdminSite(AdminSite):
#     site_title = "My Custom Admin"
#     site_header = "Admin Panel"
#     index_title = "Dashboard"

#     def sidebar_menu(self, request):
#         return [
#             {
#                 "name": _("Dashboard"),
#                 "icon": "fas fa-home",
#                 "url": reverse("admin:index"),
#                 "permissions": ["auth.view_user"],
#             },
#             {
#                 "name": _("Users"),
#                 "icon": "fas fa-users",
#                 "url": get_admin_url("auth", "user"),
#                 "permissions": ["auth.view_user"],
#             },
#             {
#                 "name": _("Products"),
#                 "icon": "fas fa-box-open",
#                 "url": get_admin_url("shop", "product"),
#                 "permissions": ["shop.view_product"],
#             },
#             {
#                 "name": _("Orders"),
#                 "icon": "fas fa-shopping-cart",
#                 "url": get_admin_url("shop", "order"),
#                 "permissions": ["shop.view_order"],
#             },
#             {
#                 "name": _("Settings"),
#                 "icon": "fas fa-cogs",
#                 "url": "/admin/settings/",
#             },
#         ]

# custom_admin_site = CustomAdminSite(name="custom_admin")
