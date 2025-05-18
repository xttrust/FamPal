from django.shortcuts import render, get_object_or_404
from .models import FamilyGroup

def family_list(request):
    families = FamilyGroup.objects.all()
    return render(request, 'families/family_list.html', {'families': families})

def family_detail(request, pk):
    family = get_object_or_404(FamilyGroup, pk=pk)
    return render(request, 'families/family_detail.html', {'family': family})
