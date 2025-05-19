from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FamilyGroup

def family_list(request):
    families = FamilyGroup.objects.all()
    return render(request, 'families/family_list.html', {'families': families})

def family_detail(request, pk):
    family = get_object_or_404(FamilyGroup, pk=pk)
    return render(request, 'families/family_detail.html', {'family': family})

@login_required
def add_question(request, family_pk):
    family = get_object_or_404(FamilyGroup, pk=family_pk)
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Question.objects.create(user=request.user, family_group=family, text=text)
    return redirect('family_detail', pk=family_pk)

@login_required
def add_answer(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Answer.objects.create(question=question, user=request.user, text=text)
    return redirect('help')