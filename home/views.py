import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from families.models import FamilyGroup, Question
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        reason = request.POST.get('reason')
        message = request.POST.get('message')

        success = True  # Set success flag if form submitted

    return render(request, 'home/contact.html', {'success': success})

@login_required
def help(request):
    family = FamilyGroup.objects.first()  # Or get based on user

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Question.objects.create(user=request.user, family_group=family, text=text)
            return redirect('help')  # Redirect to avoid resubmission

    questions = family.questions.all() if family else []

    return render(request, 'home/help.html', {
        'family': family,
        'questions': questions,
    })
