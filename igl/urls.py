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
    
    path('gallery/',views.gallery,name="gallery"),
    path('case_studies/',views.case_studies,name="case_studies"),
    
    path('career/',views.career,name="career"),
    
    path('blog/',views.blog,name="blog"),
    path('blog_single/<int:pk>/',views.blog_single,name="blog_single"),
    
    
    
   
    
]