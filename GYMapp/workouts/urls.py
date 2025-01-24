
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
    path('workouts',views.add_workout,name='workouts'),
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('member_workouts',views.member_workouts,name='member_workouts'),



]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
