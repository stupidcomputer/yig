import fitz
import math

from typing import Any

class FitzBlockWrapper:
    def __init__(self, block):
        self.x0, self.y0, self.x1, \
            self.y1, self.text, \
            self.block_number, self.block_type = block

        self.x0 = int(self.x0)
        self.x1 = int(self.x1)
        self.y0 = int(self.y0)
        self.y1 = int(self.y1)
        self.block_number = int(self.block_number)
        self.block_type = int(self.block_type)

    def __str__(self):
        return str((
            self.x0, self.y0, self.x1, self.y1, self.text
        ))

    def __repl__(self):
        return self.__str__()

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
            self.color = "red"
        elif self.color == "W":
            self.color = "white"
        elif self.color == "B":
            self.color = "blue"

        assemblydivision = assemblycode[1]
        if assemblydivision == "S":
            self.assembly = "senate"
        elif assemblydivision == "H":
            self.assembly = "house"

        self.year = int(dashsplit[0])
        self.committee = int(dashsplit[1])
        self.docketplacement = int(dashsplit[2])

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
        school: str
    ):
        if isinstance(code, str):
            self.code = BillCode(code)
        else:
            self.code = code

        self.sponsors = sponsors.rstrip()
        self.subcommittee = subcommittee.rstrip()
        self.school = school.rstrip()

class PdfParser:
    def __init__(self, document: fitz.Document):
        self.document = document

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
            print("page number {} contains sentintal? {}".format(page.number, is_section_page))
            if len(page.get_images()) == 3:
                print("page {} has one image!".format(page.number))
                print(page.get_images())

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

            joined_blocks += block_info

        joined_blocks = self._remove_image_blocks(joined_blocks)
        joined_blocks = self._remove_coordinate_information(joined_blocks)

        bill_header = joined_blocks[0]

        splitted = self._split_list_by_element(joined_blocks, bill_header)

        count = 0
        for i in splitted:
            if count < 20:
                print(i)
            count += 1
