from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from members.models import Member
from trainer.models import Trainer
from packages.models import Packages
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, fields
from datetime import timedelta
from django.db.models import Sum
from django.utils.timezone import now
from payment.models import Payment
# Create your views here.

def dashboard(request):
    today = timezone.now().date()

    # Use ExpressionWrapper to calculate the expiry date
    active_members = Member.objects.annotate(
        expiry_date=ExpressionWrapper(F('starting_date') + ExpressionWrapper(F('package__duration') * timedelta(days=1),
                output_field=fields.DurationField()),
            output_field=fields.DateField())).filter(expiry_date__gt=today)
    #member count
    members=Member.objects.all().count()

    male_members=Member.objects.filter(gender='Male').count()
    female_members=Member.objects.filter(gender='Female').count()
    #monthly & anual income 
    monthly_income = monthly_income_data()
    annual_income = sum(monthly_income)
    single_monthly_income=monthly_incomee()
    # Pass the count of active members to the template
    context = {
        'active_members': active_members,
        'active_members_count': active_members.count(),
        'members':members,
        'male_members':male_members,
        'female_members':female_members,
        'monthly_income':monthly_income,
        'annual_income':annual_income,
        'single_monthly_income':single_monthly_income
    }
    return render(request,'dashboard.html',context)

def index(request):
    return render(request,'index.html')

def register(request):
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
            return redirect(login)
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
    return render(request,'register.html',context)

#calculating monthly & anual income
def monthly_incomee():
    current_month = now().month
    current_year = now().year
    return Payment.objects.filter(created_at__year=current_year, created_at__month=current_month).aggregate(Sum('amount'))['amount__sum']


def monthly_income_data():
    current_year = now().year
    monthly_income = []
    
    for month in range(1, 13):
        income = Payment.objects.filter(
            created_at__year=current_year, created_at__month=month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_income.append(income)

    return monthly_income

def annual_income():
    current_year = now().year
    return Payment.objects.filter(created_at__year=current_year).aggregate(Sum('amount'))['amount__sum']


