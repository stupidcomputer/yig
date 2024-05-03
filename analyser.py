import leglib
import fitz

leglib.PdfParser(fitz.open("YIGVolunteerBook2024.pdf")).parse()
