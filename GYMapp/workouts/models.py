from django.db import models
from members.models import Member
from trainer.models import Trainer
class Day(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    name = models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True,related_name="workouts")
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)  # Workout title (e.g., "Chest Press")
    description = models.TextField(blank=True, null=True)  # Optional details
    video = models.FileField(upload_to="workouts/videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.day.name} ({self.trainer})"

    class Meta:
        ordering = ['day', 'title']  # Order workouts by day and title
