from django.db import models
from django.utils.translation import gettext_lazy as _

class LegislationBook(models.Model):
    class ConferenceType(models.TextChoices):
        MIDDLE = "M", _("Middle School")
        HIGH = "H", _("High School")

    conference_type = models.CharField(
        max_length=1,
        choices=ConferenceType.choices,
        default=ConferenceType.HIGH,
    )
    pdf = models.FileField(upload_to="uploads/")
    name = models.CharField(max_length=256)
    import_strategy = models.CharField(max_length=128)

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
        return "{}/{}-{}".format(
            self.assembly,
            self.committee,
            self.docket_order,
        )
