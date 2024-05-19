import leglib

parser = leglib.parsers.HSYIGPdfParser.from_filename(
    filename="YIGVolunteerBook2024.pdf",
    confname="YIGVolunteer"
)
parser.parse()
print([i.bill_text for i in parser.bills])
