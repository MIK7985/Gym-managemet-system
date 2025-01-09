from django.db import models
from django.contrib.auth.models import User
from members.models import Member

class Payment(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
