import os
from django.shortcuts import render
from django.http import HttpResponse


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

def help(request):
    return render(request, 'home/help.html')