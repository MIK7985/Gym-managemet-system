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
from . import views

urlpatterns = [
    path('show_status',views.show_status,name='show_status'),
    path('payment',views.payment,name='payment'),
    path('payed/<int:member_id>/', views.payed, name='payed'),
    path('send-notifications', views.send_expiry_notifications, name='send_expiry_notifications'),
    path('stripe-checkout', views.stripe_checkout, name='stripe_checkout'),
    path('stripe-success/<int:member_id>/', views.stripe_success, name='stripe_success'),
    path('stripe-cancel/', views.stripe_cancel, name='stripe_cancel'),

    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
