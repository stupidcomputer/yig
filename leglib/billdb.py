from .common import Bill, CCEColors, CCEAssemblies
from .parsers import BookParser

from typing import Type, Self
from dataclasses import dataclass

class QueryAny:
    """
    Use this class to indicate an Any match for attributes without an Any attribute.
    """
    pass

class SearchNotSatisified(BaseException):
    pass

class QueryAll:
    pass

class QueryField:
    Any = object()
    Colors = CCEColors
    Assemblies = CCEAssemblies

@dataclass
class BillQuery:
    """
    Holds a query for the BillDB.
    """
    color: CCEColors | QueryField = QueryField.Any
    assembly: CCEAssemblies | QueryField = QueryField.Any
    committee: int | QueryField = QueryField.Any
    year: int | QueryField = QueryField.Any
    subcommittee: str | QueryField = QueryField.Any
    sponsors: str | QueryField = QueryField.Any
    school: str | QueryField = QueryField.Any
    bill_text: str | QueryField = QueryField.Any
    title: str | QueryField = QueryField.Any

    def __post_init__(self):
        self.bill_text_concat = self.bill_text # for search compat reasons

class BillDB:
    def __init__(self):
        self.bills: list[Bill] = []
        self.cache: dict[Bill]

    @staticmethod
    def code_enum_match(bill: Bill, query: BillQuery, attr: str) -> None:
        """
        This is probably very slow. Maybe replace this with a better solution?

        This function replaces repetitive code like this:

        elif bill.assembly != CCEAssemblies.Any:
            if bill.assembly != query.color:
                raise SearchNotSatisified()

        with this:

        self.enum_match(bill, query, "color")

        This is the case with exact_match and string_match, too.
        """

        if query.__getattribute__(attr) == QueryField.Any:
            return

        # check the Any case
        if query.__getattribute__(attr) != bill.code.__getattribute__(attr).__class__.Any:
            # make sure we're not matching
            if bill.code.__getattribute__(attr) != query.__getattribute__(attr):
                raise SearchNotSatisified()

        # if we do match, no exception

    @staticmethod
    def string_match(bill: Bill, query: BillQuery, attr: str) -> None:
        """
        See self.code_enum_match for more info.
        """
        if query.__getattribute__(attr) == QueryField.Any:
            return

        if not query.__getattribute__(attr).lower() in bill.__getattribute__(attr).lower():
            raise SearchNotSatisified()

    def add_conference(self: Self, parser: Type[BookParser]) -> None:
        """
        Type[BookParser] -> any subclass of BookParser
        """

        # this works because each BookParser must insert its self.confname into its self.bills[i].code.conference field.
        self.bills += parser.bills

    def search(self: Self, query: BillQuery | QueryAll) -> list[Bill]:
        if query == QueryAll:
            return self.bills
        results = []
        for bill in self.bills:
            try:
                self.code_enum_match(bill, query, "color")
                self.code_enum_match(bill, query, "assembly")

                if not query.committee == QueryField.Any:
                    if not query.committee == bill.code.committee:
                        raise SearchNotSatisified()

                if not query.committee == QueryField.Any:
                    if not query.year == bill.code.year:
                        raise SearchNotSatisified()

                self.string_match(bill, query, "subcommittee")
                self.string_match(bill, query, "sponsors")
                self.string_match(bill, query, "school")
                self.string_match(bill, query, "bill_text_concat")
                self.string_match(bill, query, "title")

            except SearchNotSatisified:
                continue
            results.append(bill)

        return results
