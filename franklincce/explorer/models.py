from django.db import models
from django.utils.translation import gettext_lazy as _

from .leglib import HSYIG24, HSMUN23
import io
import fitz

from collections import namedtuple

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
            print(text["code"])
            codesplit = text["code"].split('/')
            assembly = codesplit[0]
            dashsplit = codesplit[1].split('-')
            year = 2000 + int(dashsplit[0])
            committee = int(dashsplit[1])
            docket_order = int(dashsplit[2])
            text = LegislativeText(
                assembly=assembly,
                year=year,
                committee=committee,
                docket_order=docket_order,
                school=text["school"],
                sponsors=text["sponsors"],
                legislation_title=text["title"],
                text=text["bill_text"],
                from_book=self
            )
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
    docket_order = models.IntegerField()
    school = models.CharField(max_length=256)
    sponsors = models.CharField(max_length=256)
    from_book = models.ForeignKey(LegislationBook, on_delete=models.CASCADE)
    legislation_title = models.CharField(max_length=512)
    country = models.CharField(
        max_length=512,
        null=True,
        blank=True
    )

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
