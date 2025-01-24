from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Workout, Day, Trainer, Member
from django.db.models import Count



@login_required
def add_workout(request):
    trainer = Trainer.objects.get(user=request.user)  # Ensure the logged-in user is a trainer

    if request.method == 'POST' and 'register' in request.POST:
        try:
            # Fetch form data
            member_id = request.POST.get('member')  # ID of the member
            title = request.POST.get('title')
            description = request.POST.get('description')
            day_name = request.POST.get('day')  # Day of the workout (e.g., "Monday", "Tuesday", etc.)
            video = request.FILES.get('video')  # Video file, if uploaded

            # Get the member object
            member = Member.objects.get(id=member_id, trainer=trainer)  # Ensure the member belongs to this trainer

            # Get the day object
            day = Day.objects.get(name=day_name)  # Get the Day object by name

            # Check if workout for this day already exists for the member
            if Workout.objects.filter(member=member, day=day, title=title).exists():
                messages.error(request, f"A workout with the title '{title}' already exists for {day_name}.")
            else:
                # Create the workout if title is unique
                Workout.objects.create(
                    trainer=trainer,
                    member=member,
                    title=title,
                    description=description,
                    day=day,
                    video=video,
                )
                messages.success(request, "Workout added successfully!")

        except Member.DoesNotExist:
            messages.error(request, "Invalid member selected or unauthorized access.")
        except Day.DoesNotExist:
            messages.error(request, "Invalid day selected.")
        except Exception as e:
            # Log the error for debugging in production
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error while creating workout: {e}")
            messages.error(request, "Error occurred during workout creation. Please try again.")
    
    # Fetch workouts and paginate them
    workout_list = Workout.objects.filter(trainer=trainer).order_by('-created_at')  # Show only the trainer's workouts
    page = request.GET.get('page', 1)
    workout_paginator = Paginator(workout_list, 10)
    workouts = workout_paginator.get_page(page)

    # Fetch members assigned to this trainer
    members = trainer.members.all()
    selected_member = None
    workouts_by_day = {}

    # Check if a member ID is passed to fetch their workouts
    member_id = request.GET.get('member_id')
    if member_id:
        selected_member = get_object_or_404(Member, id=member_id, trainer=trainer)
        workouts = selected_member.workouts.all().order_by('day')  # Order by day
        for workout in workouts:
            if workout.day.name not in workouts_by_day:
                workouts_by_day[workout.day.name] = []
            workouts_by_day[workout.day.name].append(workout)


    days_of_week = Day.objects.all()  # Get all the days (Monday, Tuesday, etc.)
    context = {
        'workouts_by_day': workouts_by_day,
        'selected_member': selected_member,
        'members': members,
        'days_of_week': days_of_week,
    }

    return render(request, 'workout.html', context)




def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    
    if request.method == "POST":
            # Delete video file if it exists

            workout.delete()
            messages.success(request, 'Workout deleted successfully.')
            return redirect('workouts')  # Ensure this is the correct redirect URL



def member_workouts(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if the user is not logged in

    # Fetch the member instance related to the logged-in user
    member = get_object_or_404(Member, user=request.user)

    # Group workouts by day
    workouts_by_day = Workout.objects.filter(member=member).select_related('day').order_by('day__name')

    # Organize workouts by day (using a dictionary)
    workouts_grouped_by_day = {}
    for workout in workouts_by_day:
        day_name = workout.day.name
        if day_name not in workouts_grouped_by_day:
            workouts_grouped_by_day[day_name] = []
        workouts_grouped_by_day[day_name].append(workout)

    return render(request, 'member_workouts.html', {
        'workouts_by_day': workouts_grouped_by_day,
    })
