from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from families.models import FamilyGroup, Question

@login_required
def profile_view(request):
    user = request.user
    # Group the user created
    group_created = FamilyGroup.objects.filter(created_by=user).first()
    # Group they are a member of
    groups_joined = user.family_memberships.select_related('family_group').all()
    # Questions they asked
    user_questions = user.questions.all()
    # Group questions if in group
    group_questions = Question.objects.filter(family_group__in=[group.family_group for group in groups_joined]) if groups_joined else []

    return render(request, 'userprofile/profile.html', {
        'user': user,
        'group_created': group_created,
        'groups_joined': groups_joined,
        'user_questions': user_questions,
        'group_questions': group_questions,
    })
