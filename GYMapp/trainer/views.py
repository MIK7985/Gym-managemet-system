from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Trainer
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
def add_Trainer(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
          

            # Create user account
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            Trainer_group = Group.objects.get(name='Trainer')
            user.groups.add(Trainer_group)

            # Create Trainer instance
            Trainer.objects.create(
                user=user,
                name=name,
                address=address,
                phone=phone,
                gender=gender,
            )
            messages.success(request, "Trainer registered successfully!")
        except Exception as e:
            print(f"Error while creating Trainer: {e}")
            messages.error(request, "Error occurred during registration. Please try again.")
    
    # Fetch Trainers and form options
    Trainer_list = Trainer.objects.all()
    page = request.GET.get('page', 1)
    Trainer_paginator = Paginator(Trainer_list, 10)
    Trainer_list = Trainer_paginator.get_page(page)
  

    context = {
        'trainers': Trainer_list,
    }

    return render(request, 'trainers.html', context)




@user_passes_test(is_admin)
def update_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)

    if request.method == 'POST':
        trainer.name = request.POST.get('name')
        trainer.address = request.POST.get('address')
        trainer.phone = request.POST.get('phone')
        trainer.gender = request.POST.get('gender')
      

        trainer.save()
        messages.success(request, "Member updated successfully!")
        return redirect('trainer')  # Redirect to the list of members

    context = {
        'member': trainer,
    }
    return render(request, 'update_member.html', context)
 



@user_passes_test(is_admin)
def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)

    if request.method == 'POST':
        trainer.delete()
        messages.success(request, "Trainer removed successfully!")
        return redirect('trainer')  # Redirect to the list of trainers

    return redirect('trainer')  # Redirect if not a POST request
