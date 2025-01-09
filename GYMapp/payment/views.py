from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from members.models import Member
from trainer.models import Trainer
from packages.models import Packages
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.core.mail import send_mail  # Ensure to import this for sending emails
from django.utils.timezone import now
from .models import Payment
import stripe
from django.conf import settings
# Create your views here.

@login_required
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


@login_required
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


@login_required
def payed(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and int(amount) > 0:
            amount = int(amount)
            
            # Deduct amount from member's pending_amount
            member.pending_amount -= amount
            member.save()
            
            # Create a Payment record
            Payment.objects.create(
                member=member,
                amount=amount,
                status='completed',  # Or any other status logic you need
                created_at=now()
            )
            
            messages.success(request, "Payment recorded successfully.")
        else:
            messages.error(request, "Invalid payment amount.")
        return redirect(reverse('payment'))


#notifications

@login_required
def send_expiry_notifications(request):
    # Get the current date for comparison
    current_date = timezone.now().date()
    # Fetch all members
    members = Member.objects.all()
    expired_members = []
    
    # Check each member's package expiry
    for member in members:
        if member.package_expiry() <= 0:  # If the package has expired
            expired_members.append(member)

    # Sending emails and WhatsApp messages to expired members
    for member in expired_members:
        send_expiry_email(member)
        #send_whatsapp_message(member)

    # Provide feedback after sending notifications
    messages.success(request, 'Notifications sent to expired members.')

    # Redirect to the member list or any desired page
    return redirect('member')


def send_expiry_email(member):
    subject = 'Your Gym Package has Expired'
    message = f"Hi {member.name},\n\nYour gym package has expired. Please renew your subscription to continue your training."
    email_from = 'mikwebsites@gmail.com'  # Replace with your email
    recipient_list = [member.user.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f'Email sent to {member.name} at {member.user.email}.')
    except Exception as e:
        print(f'Error sending email: {e}')





stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def stripe_checkout(request):
    member = get_object_or_404(Member, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount.isdigit() and int(amount) > 0:
            amount = int(amount) * 100  # Stripe processes amounts in cents
            
            try:
                # Create a Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f"Payment for {member.name}",
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(
                        reverse('stripe_success', args=[member.id]) + f"?amount={amount // 100}"
                    ),
                    cancel_url=request.build_absolute_uri(reverse('stripe_cancel')),
                )
                return redirect(session.url)
            except stripe.error.StripeError as e:
                messages.error(request, f"Stripe error: {str(e)}")
        else:
            messages.error(request, "Invalid payment amount.")
    return render(request, 'stripe_checkout.html', {'member': member})




@login_required
def stripe_success(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    amount = request.GET.get('amount')

    try:
        # Convert the amount to an integer and ensure it's valid
        amount = int(amount)
        if amount > 0:
            # Update the member's pending amount
            if member.pending_amount is not None:  # Ensure it's not null
                member.pending_amount = max(0, member.pending_amount - amount)
                member.save()

            # Log the payment in the Payment model
            Payment.objects.create(
                member=member,
                amount=amount,
                status='completed',
                stripe_payment_id=request.GET.get('payment_intent', ''),  # Optional
            )

            messages.success(request, "Payment was successful!")
        else:
            messages.error(request, "Invalid payment amount.")
    except (ValueError, TypeError):
        messages.error(request, "Invalid payment amount format.")

    return redirect('member_profile')




@login_required
def stripe_cancel(request):
    messages.error(request, "Payment was canceled.")
    return redirect('payment')
