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

def view_conference(request, conference_id):
    book = get_object_or_404(LegislationBook, pk=conference_id)
    results = LegislativeText.objects.filter(from_book=book)
    context = {
        "book": book,
        "legislation": results,
        "sample": results[0]
    }
    return render(request, "explorer/conference.html", context)

def stats(request):
    all_legislation = len(LegislativeText.objects.all())
    context = {
        "all":          all_legislation,
        "red_senate":   len(LegislativeText.objects.filter(assembly="RSB")),
        "blue_senate":  len(LegislativeText.objects.filter(assembly="BSB")),
        "white_senate": len(LegislativeText.objects.filter(assembly="WSB")),
        "red_house":    len(LegislativeText.objects.filter(assembly="RHB")),
        "blue_house":   len(LegislativeText.objects.filter(assembly="BHB")),
        "white_house":  len(LegislativeText.objects.filter(assembly="WHB")),
        "red_ga":       len(LegislativeText.objects.filter(assembly="RGA")),
        "blue_ga":      len(LegislativeText.objects.filter(assembly="BGA")),
        "white_ga":     len(LegislativeText.objects.filter(assembly="WGA")),
    }
    return render(request, "explorer/stats.html", context)
