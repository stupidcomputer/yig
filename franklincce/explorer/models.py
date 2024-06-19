from django.db import models
from django.utils.translation import gettext_lazy as _

from .lib.parsers import HSYIG, HSMUN
import io
import fitz

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
        super().save(**kwargs)

        if not self.has_performed_export:
            self.has_performed_export = True
            super().save(**kwargs)
        else:
            return

        the_file = io.BytesIO(self.pdf.file.file.read())
        the_document = fitz.open(stream=the_file)
        if self.import_strategy == "HSYIGBookParser":
            parsed = HSYIG(the_document)
        elif self.import_strategy == "HSMUNBookParser":
            parsed = HSMUN(the_document)
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

    def __str__(self):
        return "{}/{}-{}-{}".format(
            self.assembly,
            str(self.year),
            self.committee,
            self.docket_order,
        )
