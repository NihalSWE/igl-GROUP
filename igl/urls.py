from . import views
from . import admin_views
from django.urls import path


urlpatterns = [

    path('',views.home,name="home"),
    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    
    # path('igl_web/',views.igl_web,name="igl_web"),
    
    path('bod/',views.bod,name="bod"),
    path('bod/member/<slug:slug>/', views.bod_single, name='bod_single'),  # Display single member
    path('bos/',views.bos,name="bos"),
    path('bos/member/<slug:slug>/', views.bos_single, name='bos_single'),  # Display single member
    
    path('contact/',views.contact,name="contact"),
    path('address/', views.address, name='address'),
    path('feedback/', views.feedback, name='feedback'),
    path('location-map/', views.location_map, name='location_map'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/album/<slug:album_slug>/', views.album_images, name='album_images'),  # Use slug instead of id
    path('vdo_gly/',views.vdo_gly,name="vdo_gly"),
    
    
    path('Bussiness/',views.Bussiness,name="Bussiness"),
    # path('iglweb/', views.igl_web, name='igl_web'),
    # path('iglhost/', views.igl_host, name='igl_host'),
    # path('studentvisa/', views.stdnt_visa, name='stdnt_visa'),
    # path('felnatech/', views.felnatech, name='felnatech'),
    path('sister-concern/<slug:slug>/', views.sister_concern_single, name='sister_concern_single'),
    
    
    path('career/', views.career, name='career'),
    path('job_detail/<int:pk>/', views.job_detail, name='job_detail'),  # Ensure this is present
    path('submit_application/<int:job_id>/', views.submit_application, name='submit_application'),
    
    # path('blog/',views.blog,name="blog"),
    # path('blog_single/<int:pk>/',views.blog_single,name="blog_single"),
    
    
    path('our_customer/',views.our_customer,name="our_customer"),
    path('policy/',views.policy,name="policy"),
    path('terms/',views.terms,name="terms"),
    
    path('check_application/', views.check_application, name='check_application'),



    # Admin URLS
    path('admin_home/', admin_views.admin_home, name='admin_home'),
    path('admin_home_banner/', admin_views.admin_home_banner, name='add_home_banner'),


    path('home-banners/', admin_views.home_banner_list, name='home_banner_list'),
   
    path('home-banner/edit/<int:banner_id>/', admin_views.edit_home_banner, name='edit_home_banner'),
    path('home-banner/delete/<int:banner_id>/', admin_views.delete_home_banner, name='delete_home_banner'),



    path('home_intro_form/', admin_views.home_intro_form, name='home_intro_form'),
    path('industry_form/', admin_views.industry_form, name='industry_form'),

    path('industry/', admin_views.industry_list, name='industry_list'),  # List industries
    path('industry/edit/<int:industry_id>/', admin_views.edit_industry, name='edit_industry'),  # Edit an industry
    path('industry/delete/<int:industry_id>/', admin_views.delete_industry, name='delete_industry'),  # Delete an industry
    path('add_reason_to_choose/', admin_views.add_reason_to_choose, name='add_reason_to_choose'),
    path('reason_to_choose/', admin_views.reason_to_choose_list, name='reason_to_choose_list'),
    path('edit_reason_to_choose/<int:reason_id>/', admin_views.edit_reason_to_choose, name='edit_reason_to_choose'),
    path('delete_reason_to_choose/<int:reason_id>/', admin_views.delete_reason_to_choose, name='delete_reason_to_choose'),




    path('about_banner_form/', admin_views.about_banner_form, name='about_banner_form'),
    path('about_section_form/', admin_views.about_section_form, name='about_section_form'),
    path('gallery_banner_form/', admin_views.gallery_banner_form, name='gallery_banner_form'),
    path('gallery_album_form/', admin_views.gallery_album_form, name='gallery_album_form'),
    path('gallery-album/list/', admin_views.gallery_album_list, name='gallery_album_list'),
 # For adding a new album
    path('gallery-album/edit/<int:album_id>/', admin_views.gallery_album_edit, name='gallery_album_edit'),  # For editing an existing album
    path('gallery-album/delete/<int:album_id>/', admin_views.gallery_album_delete, name='gallery_album_delete'),
        # For deleting an album
    path('gallery-album-details/add/', admin_views.gallery_album_details, name='gallery_album_details'),
    
    # URL for listing all gallery album details
    path('gallery-album-details/list/', admin_views.gallery_album_details_list, name='gallery_album_details_list'),
    
    # URL for editing a specific gallery album detail
    path('gallery-album-details/edit/<int:detail_id>/', admin_views.edit_gallery_album_detail, name='edit_gallery_album_detail'),
    
    # URL for deleting a specific gallery album detail
    path('gallery-album-details/delete/<int:detail_id>/', admin_views.delete_gallery_album_detail, name='delete_gallery_album_detail'),


    #vedio
    path('manage_videos/', admin_views.manage_videos, name='manage_videos'),
    path('delete_video/<int:video_id>/', admin_views.delete_video, name='delete_video'),


    path('career-images/', admin_views.career_image_list, name='career_image_list'),
    path('career_images/', admin_views.career_images, name='career_images'),
    path("career-images/<int:id>/edit/",  admin_views.edit_career_image, name="edit_career_image"),
    path('delete_career_image/<int:id>/', admin_views.delete_career_image, name='delete_career_image'),

    # path('career-images/edit/<int:image_id>/', admin_views.edit_career_image, name='edit_career_image'),
    # path('career-images/delete/<int:image_id>/', admin_views.delete_career_image, name='delete_career_image'),

    path('career-banner/', admin_views.career_banner_form, name='career_banner_form'),

    path('job-postings/', admin_views.job_posting_list, name='job_posting_list'),
     path('job_posting/', admin_views.add_job_posting, name='add_job_posting'),
    path('job_posting/<int:id>/edit/', admin_views.edit_job_posting, name='edit_job_posting'),
    path('job_posting/<int:id>/delete/',admin_views.delete_job_posting, name='delete_job_posting'),
    
    
    

    path('job-applications/', admin_views.job_application_list, name='job_application_list'),
    path('job-application/add/', admin_views.add_job_application, name='add_job_application'),
    path('job-application/edit/<int:application_id>/', admin_views.edit_job_application, name='edit_job_application'),
    path('job-application/delete/<int:application_id>/', admin_views.delete_job_application, name='delete_job_application'),

    path('our-team-banner/', admin_views.our_team_banner_form, name='our_team_banner_form'),
    # Manage Board of Directors (BOD)
    path('manage_bod/', admin_views.manage_bod, name='manage_bod'),
    path('edit_bod/<slug:slug>/', admin_views.edit_bod, name='edit_bod'),
    path('delete_bod/<slug:slug>/', admin_views.delete_bod, name='delete_bod'),
    # Manage Board of Staff
    path('manage_staff/', admin_views.manage_staff, name='manage_staff'),
    path('edit_staff/<slug:slug>/', admin_views.edit_staff, name='edit_staff'),
    path('delete_staff/<slug:slug>/', admin_views.delete_staff, name='delete_staff'),



    path('locations/', admin_views.location_list, name='location_list'),
    path('locations/add/', admin_views.add_location, name='add_location'),
    path('locations/edit/<int:id>/', admin_views.edit_location, name='edit_location'),
    path('locations/delete/<int:id>/', admin_views.delete_location, name='delete_location'),

     path('contact-banner/', admin_views.contact_banner_form, name='contact_banner_form'),
    path('contacts/', admin_views.contact_list, name='contact_list'),


    path('contacts/view/<int:id>/', admin_views.view_contact, name='view_contact'),


    path('contacts/delete/<int:id>/', admin_views.delete_contact, name='delete_contact'),

    path('sister_concern_banner_form/', admin_views.sister_concern_banner_form, name='sister_concern_banner_form'),
    path('sister_concern_add/', admin_views.sister_concern_add, name='sister_concern_add'),
    path("sister-concerns/", admin_views.sister_concern_list, name="sister_concern_list"),
    path("sister-concern/edit/<slug:slug>/", admin_views.edit_sister_concern, name="edit_sister_concern"),
    path("sister-concern/delete/<slug:slug>/", admin_views.delete_sister_concern, name="delete_sister_concern"),

    path('upload/', admin_views.upload_image, name='ckeditor_upload'),  # Image upload URL
    
    
    
    
    path('login', admin_views.login_view, name='login'),  # Updated from 'admin_login'
    path('logout', admin_views.logout_view, name='logout'),  # Updated from 'admin_logout'
    path('dashboard/', admin_views.dashboard, name='dashboard'),  # Updated from 'admin_dashboard'
]