from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance
from django.contrib.auth.models import User

@csrf_exempt
def log_attendance(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        Attendance.objects.create(user=user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'}, status=400)

from django.shortcuts import render
from .models import Attendance

def attendance_view(request):
    records = Attendance.objects.all()
    return render(request, 'attendance.html', {'attendance_records': records})

