from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Member
from trainer.models import Trainer
from packages.models import Packages
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

def is_member(user):
    return user.groups.filter(name='Member').exists()

@login_required(login_url='login')
def signout_member(request):
    logout(request)
    return redirect('login')


def login_member(request):
    context = {}    
    if request.method == 'POST' and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('show_status')  # Redirect to the members page
        else:
            error_message = "Invalid credentials"
            messages.error(request, error_message)

    return render(request, 'login.html', context)

@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            dob = request.POST.get('birthdate')
            starting_date = request.POST.get('starting_date')
            trainer_id = request.POST.get('trainer')
            package_id = request.POST.get('package')

            # Create user account
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
          
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            # Get related Trainer and Package instances
            trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
            package = Packages.objects.get(id=package_id) if package_id else None

            # Create Member instance
            Member.objects.create(
                user=user,
                name=name,
                address=address,
                phone=phone,
                gender=gender,
                dob=dob,
                starting_date=starting_date,
                trainer=trainer,
                package=package,
                pending_amount=package.price
            )
            messages.success(request, "Member registered successfully!")
        except Exception as e:
            print(f"Error while creating Member: {e}")
            messages.error(request, "Error occurred during registration. Please try again.")
    
    # Fetch members and form options
    member_list = Member.objects.all()
    page = request.GET.get('page', 1)
    member_paginator = Paginator(member_list, 10)
    member_list = member_paginator.get_page(page)
    trainers = Trainer.objects.all()
    packages = Packages.objects.all()

    context = {
        'members': member_list,
        'trainers': trainers,
        'packages': packages
    }

    return render(request, 'members.html', context)

@user_passes_test(is_admin)
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.address = request.POST.get('address')
        member.phone = request.POST.get('phone')
        member.gender = request.POST.get('gender')
        trainer_id = request.POST.get('trainer')
        package_id = request.POST.get('package')
        
        # Update dob only if provided
        dob = request.POST.get('birthdate')
        if dob:
            member.dob = dob

        # Get related Trainer and Package instances
        member.trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
        member.package = Packages.objects.get(id=package_id) if package_id else None

        member.save()
        messages.success(request, "Member updated successfully!")
        return redirect('member')  # Redirect to the list of members

    context = {
        'member': member,
        'trainers': Trainer.objects.all(),
        'packages': Packages.objects.all()
    }
    return render(request, 'update_member.html', context)


 


@user_passes_test(is_admin)
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.delete()
        return redirect(reverse('member'))



