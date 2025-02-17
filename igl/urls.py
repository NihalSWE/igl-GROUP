from . import views
from django.urls import path
# from .views import submit_application, fetch_user_details,check_application


urlpatterns = [

    path('',views.home,name="home"),
    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    
    path('igl_web/',views.igl_web,name="igl_web"),
    
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
    path('iglweb/', views.igl_web, name='igl_web'),
    path('iglhost/', views.igl_host, name='igl_host'),
    path('studentvisa/', views.stdnt_visa, name='stdnt_visa'),
    path('felnatech/', views.felnatech, name='felnatech'),
    
    
    
    path('career/', views.career, name='career'),
    path('job_detail/<int:pk>/', views.job_detail, name='job_detail'),  # Ensure this is present
    path('submit_application/<int:job_id>/', views.submit_application, name='submit_application'),
    
    path('blog/',views.blog,name="blog"),
    path('blog_single/<int:pk>/',views.blog_single,name="blog_single"),
    
    
    
   path('our_customer/',views.our_customer,name="our_customer"),
   path('policy/',views.policy,name="policy"),
   path('terms/',views.terms,name="terms"),
   
   
  
    path('check_application/', views.check_application, name='check_application'),
]