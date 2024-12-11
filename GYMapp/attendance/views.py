import json  # Ensure this is imported at the top
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .models import Member, Attendance

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def qr_check_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            member_id = data.get('member_id')

            member = get_object_or_404(Member, id=member_id)

            attendance, created = Attendance.objects.get_or_create(
                member=member,
                date=timezone.now().date(),
                defaults={'check_in_time': timezone.now().time()}
            )

            if not created:
                return JsonResponse({'status': 'error', 'message': 'Member has already checked in today.'}, status=400)

            return JsonResponse({'status': 'success', 'message': 'Member checked in successfully!'})

        except Member.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Member not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



@csrf_exempt
def qr_check_out(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            member_id = data.get('member_id')

            member = get_object_or_404(Member, id=member_id)

            attendance = Attendance.objects.filter(member=member, date=timezone.now().date()).first()

            if attendance and attendance.check_in_time and not attendance.check_out_time:
                attendance.check_out_time = timezone.now().time()
                attendance.save()
                return JsonResponse({'status': 'success', 'message': 'Member checked out successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Check-in first before checking out.'}, status=400)

        except Member.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Member not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



# View for manual check-in
def check_in(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    # Try to get or create today's attendance record
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


# View for manual check-out
def check_out(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    # Get today's attendance record for the member
    attendance = Attendance.objects.filter(member=member, date=timezone.now().date()).first()

    if attendance and attendance.check_in_time and not attendance.check_out_time:
        attendance.check_out_time = timezone.now().time()
        attendance.save()
        messages.success(request, "Check-out successful!")
    else:
        messages.warning(request, "Check-in first before checking out.")
    
    return redirect('member_profile')


# View to display attendance logs
def view_attendance(request):
    member = get_object_or_404(Member, user=request.user)
    attendance_logs = Attendance.objects.filter(member=member)
    context = {
        'member': member,
        'attendance_logs': attendance_logs
    }
    return render(request, 'attendance.html', context)


# QR scanner view
def scanner(request):
    return render(request, 'scanner.html')


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Attendance

def admin_attendance_logs(request):
    # Get all attendance records, ordered by date
    all_logs = Attendance.objects.all().order_by('-date')
    
    # Create paginator object
    paginator = Paginator(all_logs, 10)  # Show 10 logs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_attendance.html', {'page_obj': page_obj})
