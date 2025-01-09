from django.db import models
from members.models import Member
from django.utils import timezone

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="attendance",default=19)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.name} - {self.date}"
