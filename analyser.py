import leglib

parser = leglib.parsers.HSYIGPdfParser.from_filename("YIGVolunteerBook2024.pdf")
parser.parse()
print([i.bill_text for i in parser.bills])
