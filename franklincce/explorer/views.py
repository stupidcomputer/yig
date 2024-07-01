from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import LegislativeText, LegislationBook, LegislationClassification, School, Country

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

def get_all_classifications(request):
    classifications = LegislationClassification.objects.all()
    return render(request, "explorer/classifications.html", {
        "classifications": classifications,
    })

def get_all_classified_by_id(request, classification_id):
    classification = get_object_or_404(LegislationClassification, pk=classification_id)
    # this is very expensive; make a way for this to be cached please?

    all_texts = LegislativeText.objects.all()
    all_terms = classification.text_to_match.split(',')
    all_terms = [i.lower() for i in all_terms]

    matches = []

    for text in all_texts:
        for term in all_terms:
            if term in text.text.lower():
                matches.append(text)
                break

    return render(request, "explorer/results.html", {
        "legislation": matches,
        "result_name": "All legislation in topic {}".format(classification.name)
    })

def get_all_by_x(model):
    def wrapped(request, model_id):
        instance = get_object_or_404(model, pk=model_id)
        return render(request, "explorer/results.html", {
            "result_name": "All legislation by {}".format(instance.name),
            "legislation": instance.legislativetext_set.all()
        })
    
    return wrapped

def get_all_xs(model):
    def wrapper(request):
        instances = model.objects.all()
        try:
            # what the heck, django?????
            plural = model._meta.verbose_name_plural
        except:
            plural = model.__name__ + "s"

        plural = plural.lower()

        return render(request, "explorer/listing.html", {
            "result_name": "All {}".format(plural),
            "instances": instances,
        })

    return wrapper

def return_groups(request):
    return render(request, "explorer/by_group.html", {})

get_all_by_school = get_all_by_x(School)
get_all_by_country = get_all_by_x(Country)

get_all_schools = get_all_xs(School)
get_all_countries = get_all_xs(Country)