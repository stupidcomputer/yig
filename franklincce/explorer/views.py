from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import LegislativeText, LegislationBook

from random import sample

def index(request):
    legislative_texts = list(LegislativeText.objects.all())
    legislative_texts = sample(legislative_texts, 5)
    context = {
        "legislative_texts": legislative_texts,
    }
    return render(request, "explorer/index.html", context)

def all(request):
    legislative_texts = list(LegislativeText.objects.all())
    context = {
        "legislative_texts": legislative_texts,
    }
    return render(request, "explorer/all.html", context)

def view_legislation(request, legislation_id):
    legislation = get_object_or_404(LegislativeText, pk=legislation_id)
    context = {
        "legislation": legislation,
        "lines": legislation.get_lines()
    }
    return render(request, "explorer/legislation.html", context)
