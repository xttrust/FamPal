from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from families.models import FamilyGroup, Question, FamilyMembership
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user

    # Group the user created
    group_created = FamilyGroup.objects.filter(created_by=user).first()

    # Groups the user is a member of
    groups_joined = user.family_memberships.select_related('family_group').all()

    # Questions asked by the user
    user_questions = user.questions.all()

    # Questions in the groups the user belongs to
    group_questions = Question.objects.filter(
        family_group__in=[membership.family_group for membership in groups_joined]
    ) if groups_joined else []

    # Collect members from all joined groups using FamilyMembership
    group_members = FamilyMembership.objects.filter(
        family_group__in=[membership.family_group for membership in groups_joined]
    ).select_related('user')

    # Show create button only if no group was created or joined
    show_create_button = not group_created and not groups_joined.exists()

    return render(request, 'userprofile/profile.html', {
        'user': user,
        'group_created': group_created,
        'groups_joined': groups_joined,
        'user_questions': user_questions,
        'group_questions': group_questions,
        'group_members': group_members,
        'show_create_button': show_create_button,
    })


@login_required
def leave_family_view(request, membership_id):
    membership = get_object_or_404(FamilyMembership, id=membership_id, user=request.user)

    # Don't allow user to leave a group they created
    if membership.family_group.created_by == request.user:
        messages.warning(request, "You can't leave a group you created. You must delete it instead.")
        return redirect('profile')

    if request.method == 'POST':
        membership.delete()
        messages.success(request, "You have successfully left the family group.")
        return redirect('profile')

    return redirect('profile')
