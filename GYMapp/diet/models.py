from django.db import models
from members.models import Member
from trainer.models import Trainer
# Create your models here.

class SentDietPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='diet_plans')
    title = models.CharField(max_length=100)  # e.g., "Fat Loss Diet Plan"
    content = models.TextField()  # Diet plan details
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} sent to {self.member.user.username} by {self.trainer.user.username}"
