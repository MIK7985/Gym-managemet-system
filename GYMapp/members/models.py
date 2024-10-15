from django.db import models
from django.contrib.auth.models import User
from trainer.models import Trainer
from packages.models import Packages
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.
class Member(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) 
    name=models.CharField(max_length=200)
    address=models.TextField()
    user=models.OneToOneField(User,related_name='member_profile',on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)
    gender=models.CharField(max_length=20)
    starting_date = models.DateField(default=timezone.now)
    dob=models.DateField()
    pending_amount=models.FloatField(null=True)
    trainer=models.ForeignKey(Trainer,null=True,on_delete=models.CASCADE,related_name='trainer')
    package=models.ForeignKey(Packages,null=True,on_delete=models.CASCADE,related_name='package')
   
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def package_expiry(self):
        expiry_date = self.starting_date + timedelta(days=self.package.duration)
        remaining_days = (expiry_date - datetime.now().date()).days
        return remaining_days


    def __str__(self) -> str:
        return self.user.username
