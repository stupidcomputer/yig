import leglib #billdb import BillDB, BillQuery, QueryField, QueryAll
from leglib.billdb import BillDB, BillQuery, QueryField, QueryAll
from leglib.parsers import HSYIGPdfParser

parser = HSYIGPdfParser.from_filename(
    filename="YIGVolunteerBook2024.pdf",
    confname="HSVolunteer"
)
parser.parse()

print(len(parser.bills))

db = BillDB()
db.add_conference(parser=parser)

allbills = len(db.search(query=QueryAll))

bluelen = len(db.search(query=BillQuery(color=QueryField.Colors.Blue)))
whitelen = len(db.search(query=BillQuery(color=QueryField.Colors.White)))
redlen = len(db.search(query=BillQuery(color=QueryField.Colors.Red)))

senatelen = len(db.search(query=BillQuery(assembly=QueryField.Assemblies.Senate)))
houselen = len(db.search(query=BillQuery(assembly=QueryField.Assemblies.House)))

franklincount = len(db.search(query=BillQuery(school="Franklin")))

print(allbills)
print(redlen, whitelen, bluelen, redlen + whitelen + bluelen)
print(senatelen, houselen, senatelen + houselen)
print(franklincount)
