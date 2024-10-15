from django.shortcuts import render,redirect, get_object_or_404
from .models import Attendance, Member
from django.utils import timezone
from django.contrib import messages

def check_in(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    attendance, created = Attendance.objects.get_or_create(
        member=member,
        date=timezone.now().date(),
        defaults={'check_in_time': timezone.now().time()}
    )
    if not created:
        messages.warning(request, "Member has already checked in for today.")
    else:
        messages.success(request, "Check-in successful!")
    
    return redirect('member_profile')

def check_out(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    attendance = Attendance.objects.filter(member=member, date=timezone.now().date()).first()

    if attendance and attendance.check_in_time and not attendance.check_out_time:
        attendance.check_out_time = timezone.now().time()
        attendance.save()
        messages.success(request, "Check-out successful!")
    else:
        messages.warning(request, "Check-in first before checking out.")
    
    return redirect('member_profile')


def view_attendance(request):
    member = get_object_or_404(Member, user=request.user)
    attendance_logs = Attendance.objects.filter(member=member)
    context = {
        'member': member,
        'attendance_logs': attendance_logs
    }
    return render(request, 'attendance.html', context)


