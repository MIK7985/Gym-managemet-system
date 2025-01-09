from django.db import models
from django.contrib.auth.models import User
from trainer.models import Trainer
from packages.models import Packages
from django.utils import timezone
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.validators import RegexValidator

class Member(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    user = models.OneToOneField(User, related_name='member_profile', on_delete=models.CASCADE)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    starting_date = models.DateField(default=timezone.now)
    dob = models.DateField()
    pending_amount = models.FloatField(null=True)
    
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.CASCADE, related_name='trainer')
    package = models.ForeignKey(Packages, null=True, on_delete=models.CASCADE, related_name='package')

    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    package_expiry_date = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)  # Field to store the generated QR code image


    def package_expiry(self):
        expiry_date = self.starting_date + timedelta(days=self.package.duration)
        remaining_days = (expiry_date - datetime.now().date()).days
        print(f"Remaining days for {self.name}: {remaining_days}")  # Debugging line
        return remaining_days
    
    def save(self, *args, **kwargs):
        # Save the member first to ensure the `id` is assigned
        if not self.pk:  # If this is a new member and the primary key doesn't exist yet
            super().save(*args, **kwargs)  # Save to generate the ID
        
        # Generate QR code after the member has been saved and ID is available
        if not self.qr_code:  # Only generate if QR code isn't already set
            # Create QR code data using the unique member ID
            qr_data = f"member_id:{self.id}"
            qr_image = qrcode.make(qr_data)  # Generate QR code image
            qr_buffer = BytesIO()  # Create a BytesIO buffer to hold the image
            qr_image.save(qr_buffer, format='PNG')  # Save the image to the buffer
            qr_file = File(qr_buffer, name=f"qr_code_{self.id}.png")  # Create a Django File object
            
            # Save the QR code to the model
            self.qr_code.save(f"qr_code_{self.id}.png", qr_file)

        # Save the member again to store the QR code
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name
