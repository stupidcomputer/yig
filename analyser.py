import leglib #billdb import BillDB, BillQuery, QueryField, QueryAll

parser = leglib.parsers.HSYIGPdfParser.from_filename(
    filename="YIGVolunteerBook2024.pdf",
    confname="HSVolunteer"
)
parser.parse()

print(len(parser.bills))

db = leglib.billdb.BillDB()
db.add_conference(parser=parser)

allbills = len(db.search(query=leglib.billdb.QueryAll))

bluelen = len(db.search(query=leglib.billdb.BillQuery(color=leglib.billdb.QueryField.Colors.Blue)))
whitelen = len(db.search(query=leglib.billdb.BillQuery(color=leglib.billdb.QueryField.Colors.White)))
redlen = len(db.search(query=leglib.billdb.BillQuery(color=leglib.billdb.QueryField.Colors.Red)))

senatelen = len(db.search(query=leglib.billdb.BillQuery(assembly=leglib.billdb.QueryField.Assemblies.Senate)))
houselen = len(db.search(query=leglib.billdb.BillQuery(assembly=leglib.billdb.QueryField.Assemblies.House)))

franklincount = len(db.search(query=leglib.billdb.BillQuery(school="Franklin")))

print(allbills)
print(redlen, whitelen, bluelen, redlen + whitelen + bluelen)
print(senatelen, houselen, senatelen + houselen)
print(franklincount)
