from django.db import models

# Create your models here.

#mdel for products
class Packages(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    package_name=models.CharField(max_length=200)
    duration= models.IntegerField()  # Assuming package duration is in days
    price=models.FloatField()
    description=models.TextField()
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.package_name
    