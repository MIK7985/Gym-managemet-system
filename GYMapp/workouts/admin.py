from django.contrib import admin
from .models import Workout
from .models import Day


# Register your models here.
admin.site.register(Workout)
admin.site.register(Day)
