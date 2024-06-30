from django.db import models
from django.utils.translation import gettext_lazy as _

from .leglib import HSYIG24, HSMUN23
import io
import fitz

from collections import namedtuple

def InstantiateIfNone(model, name):
    """
    Search the model for instances by name.
    If there's none, then create one.
    """
    filtered = model.objects.filter(name__exact=name)
    try:
        return filtered[0]
    except IndexError:
        obj = model(name=name)
        obj.save()
        return obj

class School(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class LegislationBook(models.Model):
    class ConferenceType(models.TextChoices):
        MIDDLE = "M", _("Middle School")
        HIGH = "H", _("High School")

    class ImportStrategy(models.TextChoices):
        HSYIGA = "HSYIGBookParser", _("High School YIG Book Parser 1")
        HSMUNA = "HSMUNBookParser", _("High School MUN Book Parser 1")

    conference_type = models.CharField(
        max_length=1,
        choices=ConferenceType.choices,
        default=ConferenceType.HIGH,
    )
    pdf = models.FileField(upload_to="uploads/")
    name = models.CharField(max_length=256)
    import_strategy = models.CharField(
        max_length=128,
        choices=ImportStrategy.choices,
        default=ImportStrategy.HSYIGA
    )
    has_performed_export = models.BooleanField(default=False)

    def save(self, **kwargs):
        if not self.has_performed_export:
            self.has_performed_export = True
            super().save(**kwargs)
        else:
            return

        the_file = io.BytesIO(self.pdf.file.file.read())
        the_document = fitz.open(stream=the_file)
        if self.import_strategy == "HSYIGBookParser":
            parsed = HSYIG24(the_document)
        elif self.import_strategy == "HSMUNBookParser":
            parsed = HSMUN23(the_document)
        else:
            return

        for text in parsed.output:
            text["school"] = InstantiateIfNone(School, text["school"])
            if text["country"]:
                # there's sometimes "Dominican Republic" and "Dominican Republic 2"
                # handle that gracefully
                text["country"] = text["country"].replace(" 2", "")
                text["country"] = InstantiateIfNone(Country, text["country"])
            text = LegislativeText(**text, from_book=self)
            text.save()

    def __str__(self):
        return "{}".format(self.name)

class LegislativeText(models.Model):
    class Assemblies(models.TextChoices):
        RGA = "RGA", _("Red General Assembly")
        BGA = "BGA", _("Blue General Assembly")
        WGA = "WGA", _("White General Assembly")
        RHB = "RHB", _("Red House")
        BHB = "BHB", _("Blue House")
        WHB = "WHB", _("White House")
        RSB = "RSB", _("Red Senate")
        BSB = "BSB", _("Blue Senate")
        WSB = "WSB", _("White Senate")
        SEN = "SEN", _("Senate")
        HOU = "HOU", _("House")
        GEN = "GEN", _("General Assembly")

    assembly = models.CharField(
        max_length=3,
        choices=Assemblies.choices,
        default=Assemblies.GEN
    )
    text = models.TextField()
    year = models.IntegerField()
    committee = models.IntegerField()
    category = models.CharField(max_length=256)
    docket_order = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    sponsors = models.CharField(max_length=256)
    from_book = models.ForeignKey(LegislationBook, on_delete=models.CASCADE)
    legislation_title = models.CharField(max_length=512)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}/{}-{}-{}".format(
            self.assembly,
            str(self.year),
            self.committee,
            self.docket_order,
        )

    def get_lines(self):
        cls = namedtuple('LegLine', ['linenumber', 'linetext'])
        return [cls(i + 1, j) for i, j in enumerate(self.text.split('\n'))]

    def is_bill(self):
        if self.assembly in [
            "RHB",
            "BHB",
            "WHB",
            "RSB",
            "BSB",
            "WSB",
            "SEN",
            "HOU",
        ]:
            return True
        return False

    def is_resolution(self):
        if self.assembly in ["RGA", "BGA", "WGA", "GEN"]:
            return True
        return False

class LegislationClassification(models.Model):
    name = models.CharField(max_length=256, help_text="Name of this classification.")
    text_to_match = models.CharField(
        max_length=256,
        help_text="a comma seperated list of keywords to include in the classification. spaces and dashes are discluded."
    )

    def __str__(self):
        return "{}".format(self.name)
