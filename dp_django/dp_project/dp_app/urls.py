from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction, name='prediction'),
    path('history/', views.history, name='history'),
    path('upload-report/', views.upload_report, name='upload_report'), 
    path('delete-history/<int:id>/', views.delete_history, name='delete_history'),
    path('delete-all-history/', views.delete_all_history, name='delete_all_history'),
    path('aboutus/', views.about_us, name='about'),
    path('contactus/', views.contact_view, name='contact'),
    path('contact-messages/', views.contact_messages_view, name='contact_messages'),
    path('', views.user_login, name='user_login'),  # default page
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='userlogin'),

]
from django.contrib.auth.decorators import login_required