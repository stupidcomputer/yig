import leglib
import fitz

leglib.PdfParser(fitz.open("YIGVolunteerBook2024.pdf")).parse()
leglib.PdfParser.from_filename("YIGVolunteerBook2024.pdf").parse()
