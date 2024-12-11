"""
URL configuration for GYMapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from attendance import views

urlpatterns = [
    path('view_attendance', views.view_attendance, name='view_attendance'),
    path('admin_attendance_logs', views.admin_attendance_logs, name='admin_attendance_logs'),
    path('check-in/<int:member_id>/', views.check_in, name='check_in'),
    path('check-out/<int:member_id>/', views.check_out, name='check_out'),
    path('qr-check-in/', views.qr_check_in, name='qr_check_in'),
    path('qr-check-out/', views.qr_check_out, name='qr_check_out'),
    path('scanner/',  views.scanner, name='scan_qr'),  # Create this template

    

    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
