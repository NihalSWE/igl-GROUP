# admin.py
from django.contrib import admin
from .models import NavMenu, Logo,CoverSection,ContactBanner,Contact_ShedulSection, Contact_LocationSection

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
    

class Contact_LocationSectionInline(admin.TabularInline):
    model = Contact_LocationSection
    extra = 1


@admin.register(Contact_ShedulSection)
class Contact_ShedulSectionAdmin(admin.ModelAdmin):
    inlines = [Contact_LocationSectionInline]
    list_display = ("title",)







