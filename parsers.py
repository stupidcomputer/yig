import fitz
from typing import Any, Self, ClassVar
from itertools import groupby
from dataclasses import dataclass

from lib import FitzBlockWrapper
from common import Bill

@dataclass
class BookParser:
    # class variables
    humanname: ClassVar[str] = "Generic BookParser parent class."
    description: ClassVar[str] = """
        A generic description of the abilities of this BookParser.
    """

    # everything else
    document: fitz.Document
    confname: str

    @classmethod
    def from_filename(cls, filename: str, confname: str):
        return cls(
            document=fitz.open(filename),
            confname=confname
        )

class HSYIGPdfParser(BookParser):
    @staticmethod
    def _words_in_superstring(words: list[str], superstring: str) -> bool:
        for word in words:
            if not str(word).lower() in str(superstring).lower():
                return False
        return True

    def _generate_legislative_pages_list(self, sections: list[int]) -> list[int]:
        """
        sections is an array of section pages plus the last page.
        """
        current = 0
        legislative_pages: list[int] = []
        try:
            while True:
                legislative_pages += list(
                    range(
                        sections[current] + 1,
                        sections[current + 1],
                        1
                    )
                )

                current += 1
        except IndexError:
            pass

        return legislative_pages

    def _generate_section_markers(self, document: fitz.Document) -> list[int]:
        section_pages = []
        for page in document:
            text = page.get_text().encode("utf8")
            is_section_page = self._words_in_superstring(
                    words=[ "Committee", "YMCA", "Tennessee", "Youth", "in" ],
                    superstring=text
            )
            is_last_page = self._words_in_superstring(
                    words=[ "ABCs" ],
                    superstring=text
            )
#            print("page number {} contains sentintal? {}".format(page.number, is_section_page))
#            if len(page.get_images()) == 3:
#                print("page {} has one image!".format(page.number))
#                print(page.get_images())

            if is_section_page and len(page.get_images()) == 3:
                section_pages.append(page.number)

            if is_last_page and len(section_pages) > 2:
                section_pages.append(page.number)

        return section_pages

    def _get_block_info_from_page(self, page: fitz.Page):
        return [FitzBlockWrapper(i) for i in page.get_text("blocks")]

    @staticmethod
    def _remove_image_blocks(blocks: list[FitzBlockWrapper]) -> list[FitzBlockWrapper]:
        to_return: list[FitzBlockWrapper] = []
        for block in blocks:
            if block.block_type == 0:
                to_return.append(block)

        return to_return

    @staticmethod
    def _remove_coordinate_information(blocks: list[FitzBlockWrapper]) -> list[FitzBlockWrapper]:
        to_return: list[str] = []
        for block in blocks:
            to_return.append(block.text)

        return to_return

    @staticmethod
    def _get_info_from_block(block, lat: int):
        to_return = []
        for i in block:
            if math.floor(i[0]) == lat:
                to_return.append(i)
        return to_return

    @staticmethod
    def _split_list_by_element(arr: list[Any], pivot: Any):
        output = []
        current = []
        for i in arr:
            if i == pivot:
                output.append(current)
                current = []
            else:
                current.append(i)

        output.append(current)
        return output

    def parse(self):
        section_pages = self._generate_section_markers(self.document)
        legislative_pages = self._generate_legislative_pages_list(section_pages)
        joined_blocks: list[FitzBlockWrapper] = []
        for page_number in legislative_pages:
            page = self.document.load_page(page_number)
            block_info = self._get_block_info_from_page(page)

            joined_blocks += block_info[:-1] # remove the page number at the end of every page

        joined_blocks = self._remove_image_blocks(joined_blocks)
        joined_blocks = self._remove_coordinate_information(joined_blocks)

        bill_header = joined_blocks[0]

        splitted = self._split_list_by_element(joined_blocks, bill_header)

        bills: list[Bill] = []
        for splitted_item in splitted:
            try:
                bill_code, _, _, subcommittee, sponsors, school, *bill_text = splitted_item
            except ValueError:
                continue

            bill_text = ' '.join(bill_text)

#            print(type(bill_text))

            pretty_printed = self._pretty_print_bill_text(bill_text)
            bills.append(Bill(
                code=bill_code,
                subcommittee=subcommittee,
                sponsors=sponsors,
                school=school,
                bill_text=pretty_printed["bill_array"],
                title=pretty_printed["title"]
            ))

        for bill in bills: # add the conference name to each
            bill.code.conference = self.confname

        self.bills = bills

    @staticmethod
    def _find_first_line_number(bill_arrays):
        for i in range(len(bill_arrays)):
            try:
                if str(int(bill_arrays[i])) == bill_arrays[i]:
                    return i
            except ValueError:
                pass

    def _pretty_print_bill_text(self, bill_text: str):
        replaced = bill_text.replace("�", "\n")
        replaced = bill_text
        replaced = replaced.split('\n')
        replaced = [
            i \
                .replace('�', ' ') \
                .rstrip() \
                .lstrip() \
            for i in replaced
        ]

        first_line_number = self._find_first_line_number(replaced)
        title = ' '.join(replaced[:(first_line_number - 1)])
        title = ' '.join(title.split()) # remove double spaces
        rebuilt = replaced[first_line_number:][1::2]
        # remove the last line number, it doesn't have a cooresponding space at the end
        rebuilt = rebuilt[:-1]

        # remove the first line, as it's the whitespace between the title and the bill text
        rebuilt = rebuilt[1:]

        return {
            "title": title.lstrip(),
            "bill_array": rebuilt
        }
