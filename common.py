from enum import StrEnum, auto

class CCEColors(StrEnum):
    Red = "Red"
    White = "White",
    Blue = "Blue"

class CCEAssemblies(StrEnum):
    Senate = "Senate",
    House = "House",
    GeneralAssembly = "GeneralAssembly"

class BillCode:
    def __init__(self, text: str):
        # try to parse
        # codes are in this rough format: "RSB/yy-c(c)-n(n)"

        text = text.rstrip()
        slashsplit = text.split('/')
        dashsplit = slashsplit[1].split('-')

        assemblycode = slashsplit[0]

        self.color = assemblycode[0]
        if self.color == "R":
            self.color = CCEColors.Red
        elif self.color == "W":
            self.color = CCEColors.White
        elif self.color == "B":
            self.color = CCEColors.Blue

        assemblydivision = assemblycode[1]
        if assemblydivision == "S":
            self.assembly = CCEAssemblies.Senate
        elif assemblydivision == "H":
            self.assembly = CCEAssemblies.House
        elif assemblydivision == "G":
            self.assembly = CCEAssemblies.GeneralAssembly

        self.year = int(dashsplit[0])
        self.committee = int(dashsplit[1])
        self.docketplacement = int(dashsplit[2])

        self.stringrep = self.color[0].upper() + \
            self.assembly[0].upper() + \
            "B/{}-{}-{}".format(
                str(self.year),
                str(self.committee),
                str(self.docketplacement)
            )

        self.conference: None | str = None # to be filled in with BillDB

    def __str__(self):
        return "{} {} - {}-{}-{}".format(
            self.color,
            self.assembly,
            str(self.year),
            str(self.committee),
            str(self.docketplacement)
        )

class Bill:
    def __init__(self,
        code: str | BillCode,
        sponsors: str,
        subcommittee: str,
        school: str,
        bill_text: list[str],
        title: str
    ):
        if isinstance(code, str):
            self.code = BillCode(code)
        else:
            self.code = code

        self.sponsors = sponsors.rstrip()
        self.subcommittee = subcommittee.rstrip()
        self.school = school.rstrip()
        self.bill_text = bill_text
        self.title = title
