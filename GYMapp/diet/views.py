from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trainer, Member, SentDietPlan

@login_required
def send_diet_plan(request):
    """
    View to handle diet plan creation and display assigned members.
    """
    # Fetch the logged-in trainer
    trainer = get_object_or_404(Trainer, user=request.user)
    members = Member.objects.filter(trainer=trainer)

    # Get the selected member (if any)
    member_id = request.GET.get('member_id')
    selected_member = None
    diet_plans = []

    if member_id:
        selected_member = get_object_or_404(Member, id=member_id, trainer=trainer)
        diet_plans = SentDietPlan.objects.filter(member=selected_member).order_by('-sent_at')

    if request.method == "POST":
        # Handle diet plan submission
        title = request.POST.get('title')
        content = request.POST.get('content')
        member_id = request.POST.get('member')

        member = get_object_or_404(Member, id=member_id, trainer=trainer)

        SentDietPlan.objects.create(
            trainer=trainer,
            member=member,
            title=title,
            content=content
        )

        messages.success(request, f"Diet plan '{title}' sent to {member.user.username} successfully.")
        return redirect('send_diet_plan')  # Redirect to the same page

    context = {
        'members': members,
        'selected_member': selected_member,
        'diet_plans': diet_plans,
    }

    return render(request, 'send_diet.html', context)


def delete_diet(request, diet_id):
    workout = get_object_or_404(SentDietPlan, id=diet_id)
    
    if request.method == "POST":
            # Delete video file if it exists

            workout.delete()
            messages.success(request, 'diet deleted successfully.')
            return redirect('send_diet_plan')  # Ensure this is the correct redirect URL
    
@login_required
def view_received_diet_plans(request):
    member = Member.objects.get(user=request.user)
    received_diet_plans = member.diet_plans.all()

    # Process diet plan content for template
    processed_diet_plans = []
    for plan in received_diet_plans:
        content_lines = plan.content.splitlines()
        structured_content = []
        for line in content_lines:
            if ':' in line:
                time, food = line.split(':', 1)
                structured_content.append({'time': time.strip(), 'food': food.strip()})
            else:
                structured_content.append({'time': None, 'food': line.strip()})
        processed_diet_plans.append({
            'title': plan.title,
            'sent_at': plan.sent_at,
            'content': structured_content,
        })

    return render(request, 'member_diet.html', {'diet_plans': processed_diet_plans})
