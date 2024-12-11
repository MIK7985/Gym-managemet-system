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
import qrcode
from io import BytesIO
from django.core.files import File



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()

def is_member(user):
    return user.groups.filter(name='Member').exists()

@login_required(login_url='login')
def signout_member(request):
    logout(request)
    return redirect('index')


def login_member(request):
    context = {}    
    if request.method == 'POST' and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on user role
            if request.user.groups.filter(name='Admin').exists():
                return redirect('dashboard')  # Redirect to member list for admin
            elif request.user.groups.filter(name='Member').exists():
                return redirect('member_profile')  # Redirect to member profile for members
            else:
                return redirect('home')  # Default redirect if role is undefined

        else:
            error_message = "Invalid credentials"
            messages.error(request, error_message)

    return render(request, 'login.html', context)

from datetime import datetime
from django.core.files import File
import qrcode
from io import BytesIO

@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST' and 'register' in request.POST:
        try:
            profile_picture = request.FILES.get('profile_picture', None)
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

            # Convert dob and starting_date to proper date objects
            dob = datetime.strptime(dob, '%Y-%m-%d').date()  # Convert string to date
            starting_date = datetime.strptime(starting_date, '%Y-%m-%d').date()  # Convert string to date

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

            # Create Member instance and save it to get the ID
            member = Member.objects.create(
                profile_picture=profile_picture,
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

            # Save the member to get the ID
            member.save()  # Ensure the member is saved, and the ID is generated
            
            # Generate QR Code after the member ID is available
            qr_data = f"member_id:{member.id}"  # Unique data for the member
            qr_image = qrcode.make(qr_data)  # Create QR code image
            qr_buffer = BytesIO()  # Create a BytesIO buffer
            qr_image.save(qr_buffer, format='PNG')  # Save the image to the buffer
            qr_file = File(qr_buffer, name=f"qr_code_{member.id}.png")  # Create Django File object
            member.qr_code.save(f"qr_code_{member.id}.png", qr_file)  # Save the QR code to the Member instance
            member.save()  # Ensure QR code is saved to the database

            print(f"QR Code Data: {qr_data}")
            
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



@login_required
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            member.profile_picture = request.FILES['profile_picture']
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
        
        # Redirect based on user role
        if request.user.groups.filter(name='Admin').exists():
            return redirect('member')  # Redirect to member list for admin
        elif request.user.groups.filter(name='Member').exists():
            return redirect('member_profile')  # Redirect to member profile for members
        else:
            return redirect('home')  # Default redirect if role is undefined

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
    
@login_required
def member_profile(request):
    # Get the member profile for the logged-in user
    member = get_object_or_404(Member, user=request.user)
    
    context = {
        'member': member,
        'trainers': Trainer.objects.all(),
        'packages': Packages.objects.all()
    }
    return render(request, 'profile.html', context)

#profile_view
@login_required
def member_profile_single(request, member_id):
    member = get_object_or_404(Member, id=member_id)
        
    context = {
        'member': member,
        'trainers': Trainer.objects.all(),
        'packages': Packages.objects.all()
    }
    return render(request, 'member_profile.html', context)

