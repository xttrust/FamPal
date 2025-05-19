from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from families.models import FamilyGroup, Question, FamilyMembership
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.urls import reverse


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


@login_required
@require_http_methods(["POST"])
def create_family_group(request):
    user = request.user

    # Check if the user already created or joined a group
    has_created = FamilyGroup.objects.filter(created_by=user).exists()
    has_joined = FamilyMembership.objects.filter(user=user).exists()

    if has_created or has_joined:
        messages.warning(request, "You are already part of a family group and cannot create a new one.")
        return redirect('profile')

    # Create the group
    group_name = f"{user.get_full_name() or user.username}'s Family"
    family_group = FamilyGroup.objects.create(name=group_name, created_by=user)

    # Automatically add the creator as a member
    FamilyMembership.objects.create(user=user, family_group=family_group)

    messages.success(request, f"Family group '{group_name}' has been created successfully.")
    return redirect('profile')


@login_required
@require_http_methods(["POST"])
def delete_family_group(request, group_id):
    group = get_object_or_404(FamilyGroup, id=group_id)

    if group.created_by != request.user:
        messages.error(request, "You are not allowed to delete this group.")
        return redirect('profile')

    group_name = group.name

    # Delete all memberships related to the group
    FamilyMembership.objects.filter(family_group=group).delete()

    # Delete the group
    group.delete()

    messages.success(request, f"Family group '{group_name}' and all its memberships have been deleted.")
    return redirect('profile')


User = get_user_model()

@login_required
def add_family_member(request):
    """
    Adds a user by username to the family group created by the logged-in user.
    Shows appropriate messages for success, errors, or warnings.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()

        if not username:
            messages.error(request, "Please enter a username.")
            return redirect(reverse('profile'))

        # Prevent adding yourself
        if username.lower() == request.user.username.lower():
            messages.warning(request, "You cannot add yourself to the family group.")
            return redirect(reverse('profile'))

        # Try to find the user by username (case insensitive)
        try:
            user_to_add = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            messages.warning(request, f"No user found with username '{username}'.")
            return redirect(reverse('profile'))

        # Get the family group created by the current user
        try:
            family_group = FamilyGroup.objects.get(created_by=request.user)
        except FamilyGroup.DoesNotExist:
            messages.warning(request, "You do not have a family group to add members to.")
            return redirect(reverse('profile'))

        # Check if user_to_add is already a member
        if FamilyMembership.objects.filter(user=user_to_add, family_group=family_group).exists():
            messages.warning(request, f"User '{username}' is already a member of your family group.")
            return redirect(reverse('profile'))

        # Add user to family group
        FamilyMembership.objects.create(user=user_to_add, family_group=family_group)
        messages.success(request, f"User '{username}' has been added to your family group.")
        return redirect(reverse('profile'))

    # If not POST, just redirect back
    return redirect(reverse('profile'))


@login_required
def remove_family_member(request, username):
    """
    Remove a user from the current user's family group by username.
    Only the family group creator can remove members.
    """
    try:
        family_group = FamilyGroup.objects.get(created_by=request.user)
    except FamilyGroup.DoesNotExist:
        messages.error(request, "You don't have a family group.")
        return redirect(reverse('profile'))

    # Prevent removing yourself
    if username.lower() == request.user.username.lower():
        messages.warning(request, "You cannot remove yourself from the group.")
        return redirect(reverse('profile'))

    try:
        user_to_remove = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        messages.error(request, f"User '{username}' does not exist.")
        return redirect(reverse('profile'))

    membership = FamilyMembership.objects.filter(user=user_to_remove, family_group=family_group).first()

    if not membership:
        messages.warning(request, f"User '{username}' is not in your family group.")
        return redirect(reverse('profile'))

    membership.delete()
    messages.success(request, f"User '{username}' has been removed from your family group.")
    return redirect(reverse('profile'))