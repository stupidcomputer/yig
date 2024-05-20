import secrets

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from .leglib.billdb import BillDB, BillQuery, QueryField, QueryAll
from .leglib.parsers import HSYIGPdfParser

parser = HSYIGPdfParser.from_filename(
    filename="YIGVolunteerBook2024.pdf",
    confname="HSVolunteer"
)
parser.parse()
db = BillDB()
db.add_conference(parser=parser)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=str(secrets.randbelow(100000000))
    )

    Bootstrap(app)

    @app.route('/')
    def index():
        bills = db.search(query=QueryAll)
        return render_template('index.html', number_bills=len(bills), number_conferences=2, bills=bills)

    @app.route('/legislation/<conference>/<year>')
    def show_conference(conference=QueryField.Any):
        return conference

    @app.route('/legislation/<conference>/<color>/<year>')
    def show_color(
        conference=QueryField.Any,
        year=QueryField.Any,
        color=QueryField.Any,
    ):
        bills = db.search(query=BillQuery(
            color=color,
            year=int(year),
        ))
        return render_template('color.html', bills=bills)

    @app.route('/legislation/<conference>/<color>/<assembly>/<year>')
    def show_assembly(
        conference=QueryField.Any,
        assembly=QueryField.Any,
        color=QueryField.Any,
        year=QueryField.Any,
    ):
        bills = db.search(query=BillQuery(
            color=color,
            assembly=assembly,
            year=int(year),
        ))
        return render_template('assembly.html', bills=bills)

    @app.route('/legislation/<conference>/<color>/<assembly>/<year>/<committee>')
    def show_committee(
        conference=QueryField.Any,
        assembly=QueryField.Any,
        color=QueryField.Any,
        year=QueryField.Any,
        committee=QueryField.Any,
    ):
        bills = db.search(query=BillQuery(
            color=QueryField.Any,
            assembly=assembly,
            year=int(year),
            committee=int(committee),
        ))

        return render_template('committee.html', bills=bills)

    @app.route('/legislation/<conference>/<color>/<assembly>/<year>/<committee>/<order>')
    def show_bill(
        conference=QueryField.Any,
        assembly=QueryField.Any,
        color=QueryField.Any,
        year=QueryField.Any,
        committee=QueryField.Any,
        order=QueryField.Any,
    ):
        print(order, int(order))
        print(color, assembly, year, committee, order)
        bills = db.search(query=BillQuery(
            color=color,
            assembly=assembly,
            year=int(year),
            committee=int(committee),
            order=int(order),
        ))

        return render_template("bill.html", bill=bills[0])

    return app
