# admin.py
from django.contrib import admin
from .models import NavMenu, Logo,CoverSection,ContactBanner,Contact_Schedule, Contact_Location,Contact_fromdata,Gallery,GalleryBanner,Blog


@admin.register(NavMenu)
class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent', 'is_active']
    list_filter = ['parent']
    search_fields = ['name']


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['image', 'is_active']
    


@admin.register(CoverSection)
class CoverSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'button_text']
    search_fields = ['title', 'description']
    
    
    
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

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    ordering = ('-uploaded_at',)
    
#--------------blog--------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')