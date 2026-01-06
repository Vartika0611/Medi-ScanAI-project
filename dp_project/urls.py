from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from dp_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('prediction/', views.prediction, name='prediction'),
    path('history/', views.history, name='history'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('delete-history/<int:id>/', views.delete_history, name='delete_history'),
    path('delete-all-history/', views.delete_all_history, name='delete_all_history'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contact_view, name='contact'),
    path('contact-messages/', views.contact_messages_view, name='contact_messages'),
    path('', include('dp_app.urls')), 
    # 👇 Add this login URL:
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
