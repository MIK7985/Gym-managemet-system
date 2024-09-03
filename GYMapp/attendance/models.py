from django.db import models
from django.contrib.auth.models import User

class Fingerprint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fingerprint_data = models.BinaryField()  # Store fingerprint data in binary format

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
