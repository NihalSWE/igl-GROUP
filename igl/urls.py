from . import views
from django.urls import path


urlpatterns = [

    path('',views.home,name="home"),
    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    
    path('igl_web/',views.igl_web,name="igl_web"),
    
    path('bod/',views.bod,name="bod"),
    path('bos/',views.bos,name="bos"),
    
    path('contact/',views.contact,name="contact"),
    
   path('gallery/', views.gallery, name='gallery'),
    path('gallery/album/<int:album_id>/', views.album_images, name='album_images'),
    path('Bussiness/',views.Bussiness,name="Bussiness"),
    
    path('career/', views.career, name='career'),
    path('job_detail/<int:pk>/', views.job_detail, name='job_detail'),  # Ensure this is present
    path('submit_application/<int:job_id>/', views.submit_application, name='submit_application'),
    
    path('blog/',views.blog,name="blog"),
    path('blog_single/<int:pk>/',views.blog_single,name="blog_single"),
    
    
    
   
    
]