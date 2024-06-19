from .common import *
from typing import ClassVar
from dataclasses import dataclass

import fitz

class HSMUN():
    section_page_words = ["Committee", "Model", "United", "YMCA", "Tennessee", "Nations"]
    last_page_words = ["ABCs"]

    def __init__(self, document: fitz.Document):
        self.document = document
        self.__post_init__()

    def __post_init__(self):
        # run all the processing steps here
        self.parse_legislative_metablocks()

    def generate_section_markers(self) -> list[int]:
        """
        In the YIG/MUN manuals, there's section markers that delineate between the different
        committees within the manual. Let's find those, and then the last legislative page.
        """
        section_pages = []

        for page in self.document:
            text = page.get_text().encode("utf8")
            is_section_page = words_in_superstring(
                words = self.section_page_words,
                superstring = text
            )
            is_last_page = words_in_superstring(
                words = self.last_page_words,
                superstring = text
            )

            if is_section_page:
                section_pages.append(page.number)

            if is_last_page and len(section_pages) > 2:
                section_pages.append(page.number)

        return section_pages

    def get_legislative_pages(self):
        """
        Generate the section markers, then fill in the pages between them.
        """

        current = 0
        sections = self.generate_section_markers()
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

    def concat_blocks_for_leg_pages(self):
        """
        From the legislative pages, concatenate the "blocks" of text in the PDF.
        """
        blocks = []
        pages = [self.document.load_page(page_num) for page_num in self.get_legislative_pages()]
        for page in pages:
            block_info = [FitzBlockWrapper(block) for block in page.get_text("blocks")]

            blocks += block_info

        return blocks

    def split_leg_pages(self):
        """
        We have the collection of legislative page text blocks. We need
        to split them now. We split on the text "71st General Assembly...
        Youth in Government"
        """

        blocks = self.concat_blocks_for_leg_pages()
        # each item within splitted is called a "legislative meta-block"
        splitted = split_by_lambda(blocks, lambda x: "43rd General Assembly" in x.text)

        return splitted[1:] # there's an empty array at the beginning

    def handle_the_rest(self, the_rest):
        weird_character = u'\uFFFd'
        splitted_by_weird = the_rest.split(weird_character)
        title_content = ''.join(
            splitted_by_weird[0].split('\n')[:-1]
        ).rstrip().lstrip()

        bill_text = [i.split('\n')[0][1:] for i in splitted_by_weird[1:]]

        return {
            "bill_text": '\n'.join(bill_text),
            "title": title_content
        }

    def parse_legislative_metablocks(self):
        output = []
        splitted = self.split_leg_pages()
        for legislative_text in splitted:
            # there are some blocks that contain just one value
            # and are aligned to some x value on the pdf

            # it's an easy way to extract stuff
            leg_code = get_block_by_x_value(legislative_text, 88).text.rstrip()

            try:
                school = get_block_by_x_value(legislative_text, 177).text.rstrip()
            except AttributeError:
                try:
                    school = get_block_by_x_value(legislative_text, 186).text.rstrip()
                except AttributeError:
                    school = "you tell me, man"

            try:
                sponsors = get_block_by_x_value(legislative_text, 163).text.rstrip()
            except AttributeError:
                try:
                    sponsors = get_block_by_x_value(legislative_text, 166).text.rstrip()
                except AttributeError:
                    sponsors = "you tell me, man"
            try:
                subcommittee = get_block_by_x_value(legislative_text, 151).text.rstrip()
            except AttributeError:
                try:
                    subcommittee = get_block_by_x_value(legislative_text, 153).text.rstrip()
                except AttributeError:
                    subcommittee = "you tell me, man"
            the_rest = ''.join([i.text for i in legislative_text[12:]])
            print([i.text for i in legislative_text[12:]])
            handled = self.handle_the_rest(the_rest)
            title = handled["title"]
            bill_text = handled["bill_text"]

            output.append({
                "code": leg_code,
                "school": school,
                "sponsors": sponsors,
                "subcommittee": subcommittee,
                "title": title,
                "bill_text": bill_text
            })

        self.output = output
