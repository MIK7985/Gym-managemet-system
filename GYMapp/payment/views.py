from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from members.models import Member
from trainer.models import Trainer
from packages.models import Packages
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def show_status(request): 
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

    return render(request, 'status.html', context)


def payment(request): 
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

    return render(request, 'payments.html', context)


def payed(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        member.pending_amount=member.pending_amount-int(amount)
        member.save()
        return redirect(reverse('payment'))