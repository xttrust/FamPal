from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import FamilyGroup, Question, Answer

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
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Answer.objects.create(
                question=question,
                user=request.user,
                text=text,
                is_ai_generated=False  # or True depending on your logic
            )
    return redirect('help')