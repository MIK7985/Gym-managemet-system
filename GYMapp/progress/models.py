from django.core.exceptions import ValidationError
from django.db import models
from members.models import Member
from django.utils import timezone




class Progress(models.Model):
    member = models.ForeignKey(Member, related_name='progress_entries', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)  # Date of progress entry
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    body_fat_percentage = models.FloatField(null=True, blank=True, help_text="Body fat percentage")
    muscle_mass = models.FloatField(null=True, blank=True, help_text="Muscle mass in kg")
    notes = models.TextField(null=True, blank=True, help_text="Additional progress notes")
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")  # Added height field

    def clean(self):
        if self.weight is not None and self.weight < 0:
            raise ValidationError("Weight cannot be negative.")
        if self.body_fat_percentage is not None and self.body_fat_percentage < 0:
            raise ValidationError("Body fat percentage cannot be negative.")
        if self.muscle_mass is not None and self.muscle_mass < 0:
            raise ValidationError("Muscle mass cannot be negative.")
        if self.height is not None and self.height < 0:
            raise ValidationError("Height cannot be negative.")  # Validation for height

    def __str__(self):
        return f"{self.member.name} - {self.date}"

