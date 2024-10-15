from celery import shared_task
from django.utils import timezone
from members.models import Member  # Make sure to import your Member model
from .views import send_expiry_email,send_whatsapp_message

@shared_task
def check_package_expiry():
    # Get the current date for comparison
    current_date = timezone.now().date()
    # Fetch all members
    members = Member.objects.all()
    expired_members = []
    
    # Check each member's package expiry
    for member in members:
        if member.package_expiry() <= 0:  # If the package has expired
            expired_members.append(member)

    # Sending emails to expired members (You need to implement your email sending logic here)
    for member in expired_members:
        # Your email sending logic, for example:
        send_expiry_email(member)
        send_whatsapp_message(member)


