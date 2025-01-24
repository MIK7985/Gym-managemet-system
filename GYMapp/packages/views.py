from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Packages
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()

def is_Trainer(user):
    return user.groups.filter(name='Trainer').exists()


@user_passes_test(is_admin)
def add_package(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:
            package_name = request.POST.get('package_name')
            duration = request.POST.get('duration')
            price = request.POST.get('price')
            description = request.POST.get('description')
        

            # Create Trainer instance
            Packages.objects.create(
                package_name=package_name,
                duration=duration,
                price=price,
                description=description,
            )
            messages.success(request, "Package added  successfully!")
        except Exception as e:
            print(f"Error while creating Package: {e}")
            messages.error(request, "Error occurred during registration. Please try again.")
    
    # Fetch Trainers and form options
    Package_list = Packages.objects.all()
    page = request.GET.get('page', 1)
    Pckage_paginator = Paginator(Package_list, 10)
    Package_list = Pckage_paginator.get_page(page)
  

    context = {
        'packages': Package_list,
    }

    return render(request, 'packages.html', context)



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(is_admin)
def update_package(request, package_id):
    package = get_object_or_404(Packages, id=package_id)

    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        description = request.POST.get('description')

        # Update package fields
        package.package_name = package_name
        package.duration = duration
        package.price = price
        package.description = description
        package.save()

        messages.success(request, "Package updated successfully!")
        return redirect('package')  # Redirect to the package list page

    context = {
        'package': package,  # Correct variable name
    }
    return render(request, 'update_package.html', context)


@user_passes_test(is_admin)
def delete_package(request, package_id):
    package = get_object_or_404(Packages, id=package_id)

    if request.method == 'POST':
        package.delete()
        messages.success(request, "Package removed successfully!")
        return redirect('package')

    return redirect('package')





