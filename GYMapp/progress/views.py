from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from rest_framework.views import APIView  # Import APIView
from rest_framework.response import Response  # Import Response
from members.models import Member
from .models import Progress
from django.contrib import messages


from django.shortcuts import render
from .models import Progress
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

def member_progress_chart(request, member_id):
    today = timezone.now().date()
    start_date = today - timedelta(days=30)

    progress_entries = Progress.objects.filter(
        member_id=member_id,
        date__gte=start_date,
        date__lte=today
    ).order_by('date')

    dates = [entry.date for entry in progress_entries]
    weights = [entry.weight for entry in progress_entries if entry.weight is not None]
    body_fat = [entry.body_fat_percentage for entry in progress_entries if entry.body_fat_percentage is not None]
    muscle_mass = [entry.muscle_mass for entry in progress_entries if entry.muscle_mass is not None]
    
    # Calculate BMI values
    bmi_values = []
    for entry in progress_entries:
        if entry.weight is not None and entry.height is not None:
            height_meters = entry.height / 100  # Convert cm to meters
            bmi = entry.weight / (height_meters ** 2)
            bmi_values.append(round(bmi, 2))
        else:
            bmi_values.append(None)

    # Return the data as JSON
    data = {
        'labels': dates,
        'weight': weights,
        'body_fat': body_fat,
        'muscle_mass': muscle_mass,
        'bmi_values': bmi_values,
    }

    return JsonResponse(data)





def member_progress_view(request):
    member = get_object_or_404(Member, user=request.user)
    
    if request.method == 'POST':  # Handle form submission
        try:
            weight = float(request.POST.get('weight'))  # Ensure weight is a float
            height = float(request.POST.get('height'))  # Ensure height is a float

            body_fat_percentage = float(request.POST.get('body_fat_percentage'))
            muscle_mass = float(request.POST.get('muscle_mass'))
            notes = request.POST.get('notes')

            # Create Progress instance for the member
            Progress.objects.create(
                member=member,  # Link progress to the logged-in member
                weight=weight,
                body_fat_percentage=body_fat_percentage,
                muscle_mass=muscle_mass,
                notes=notes,
                height=height,
            )
            messages.success(request, "Progress added successfully!")
            return redirect('progress')  # Redirect after success

        except Exception as e:
            messages.error(request, f"Error occurred while adding progress: {e}")
            return redirect('progress')  # Redirect if error occurs

    return render(request, 'progress.html', {'member': member})
