from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import LegislativeText, LegislationBook

def index(request):
    legislative_texts = LegislativeText.objects.all()[:5]
    context = {
        "legislative_texts": legislative_texts,
    }
    return render(request, "explorer/index.html", context)

def import_books(request):
    if request.method == "GET":
        return render(request, "explorer/import.html", {})
    elif request.method == "POST":
        book = LegislationBook(
            pdf=request.FILES["bookpdf"],
            name=request.POST.get("bookname"),
            conference_type="H",
        )
        book.save()
        return render(request, "explorer/import.html", {just_imported: True})

def view_legislation(request, legislation_id):
    legislation = get_object_or_404(LegislativeText, pk=legislation_id)
    context = {
        "legislation": legislation,
    }
    return render(request, "explorer/legislation.html", context)
