from typing import Any, ClassVar
from dataclasses import dataclass

import fitz

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

def words_in_superstring(words: list[str], superstring: str) -> bool:
    for word in words:
        if not str(word).lower() in str(superstring).lower():
            return False
        return True

def split_by_lambda(arr: list[Any], func):
    output = []
    current = []
    for item in arr:
        if func(item):
            output.append(current)
            current = []
        else:
            current.append(item)

    output.append(current)
    return output

def get_block_by_x_value(arr: list[FitzBlockWrapper], xvalue: int) -> FitzBlockWrapper:
    for item in arr:
        if item.x0 == xvalue:
            return item

def remove_block_by_x_value(arr: list[FitzBlockWrapper], xvalue: int) -> list[FitzBlockWrapper]:
    return [i for i in arr if not i.x0 == xvalue]

class CCEParserBase():
    section_page_words: ClassVar[list[str]]
    last_page_words: ClassVar[list[str]]
    split_leg_pages_needle: ClassVar[str]

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
        splitted = split_by_lambda(blocks, lambda x: self.split_leg_pages_needle in x.text)

        return splitted[1:] # there's an empty array at the beginning

    def handle_the_rest(self, the_rest):
        weird_character = u''
        another_weird_character = u'\uFFFd'
        splitted_by_weird = the_rest.replace(weird_character, another_weird_character).split(another_weird_character)
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

            try:
                country = get_block_by_x_value(legislative_text, 139).text.rstrip()
                country = country.replace("Sponsor: ", "").lstrip()
            except AttributeError:
                country = None # this is a yig bill

            try:
                category = get_block_by_x_value(legislative_text, 151).text.rstrip().lstrip()
            except AttributeError:
                try:
                    category = get_block_by_x_value(legislative_text, 153).text.rstrip().lstrip()
                except AttributeError:
                    print([(i.text, i.x0) for i in legislative_text])

            leg_code = get_block_by_x_value(legislative_text, 88).text.rstrip()

            try:
                school = get_block_by_x_value(legislative_text, 177).text.rstrip().lstrip()
            except AttributeError:
                try:
                    school = get_block_by_x_value(legislative_text, 186).text.rstrip().lstrip()
                except AttributeError:
                    school = "you tell me, man"

            try:
                sponsors = get_block_by_x_value(legislative_text, 163).text.rstrip().lstrip()
            except AttributeError:
                try:
                    sponsors = get_block_by_x_value(legislative_text, 166).text.rstrip().lstrip()
                except AttributeError:
                    sponsors = "you tell me, man"

            the_rest = ''.join([i.text for i in legislative_text[12:]])
            handled = self.handle_the_rest(the_rest)
            title = handled["title"]
            bill_text = handled["bill_text"]
            
            codesplit = leg_code.split('/')
            assembly = codesplit[0]
            dashsplit = codesplit[1].split('-')
            year = 2000 + int(dashsplit[0])
            committee = int(dashsplit[1])
            docket_order = int(dashsplit[2])

            output.append({
                "assembly": assembly,
                "year": year,
                "committee": committee,
                "docket_order": docket_order,
                "category": category,
                "country": country,
                "school": school,
                "sponsors": sponsors,
                "legislation_title": title,
                "text": bill_text
            })

        self.output = output
    

class HSMUN23(CCEParserBase):
    section_page_words = ["Committee", "Model", "United", "YMCA", "Tennessee", "Nations"]
    last_page_words = ["ABCs"]
    split_leg_pages_needle = "43rd General Assembly"
    
class HSYIG24(CCEParserBase):
    section_page_words = [ "Committee", "YMCA", "Tennessee", "Youth", "in" ]
    last_page_words = [ "ABCs" ]
    split_leg_pages_needle = "71st General Assembly"

    def generate_section_markers(self) -> list[int]:
        """
        This overrides the regular method because we need to check
        for three images on a section page
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

            if is_section_page and len(page.get_images()) == 3:
                section_pages.append(page.number)

            if is_last_page and len(section_pages) > 2:
                section_pages.append(page.number)

        return section_pages

    def parse_legislative_metablocks(self):
        """
        This is YIG specific code
        """
        output = []
        splitted = self.split_leg_pages()
        for legislative_text in splitted:
            # there are some blocks that contain just one value
            # and are aligned to some x value on the pdf

            # it's an easy way to extract stuff
            legislative_text = remove_block_by_x_value(legislative_text, 565) # remove page numbers
            category = get_block_by_x_value(legislative_text, 139).text.rstrip().lstrip()
            leg_code = get_block_by_x_value(legislative_text, 88).text.rstrip()
            school = get_block_by_x_value(legislative_text, 163).text.rstrip().lstrip()
            sponsors = get_block_by_x_value(legislative_text, 152).text.rstrip().lstrip()
            the_rest = ''.join([i.text for i in legislative_text[6:]])
            handled = self.handle_the_rest(the_rest)
            title = handled["title"]
            bill_text = handled["bill_text"]

            codesplit = leg_code.split('/')
            assembly = codesplit[0]
            dashsplit = codesplit[1].split('-')
            year = 2000 + int(dashsplit[0])
            committee = int(dashsplit[1])
            docket_order = int(dashsplit[2])

            output.append({
                "assembly": assembly,
                "year": year,
                "committee": committee,
                "docket_order": docket_order,
                "category": category,
                "country": None, # this is a yig bill
                "school": school,
                "sponsors": sponsors,
                "legislation_title": title,
                "text": bill_text
            })

        self.output = output

def main():
    argv = sys.argv
    doc = fitz.open(argv[1])
    if argv[2] == "HSYIG":
        doc = HSYIG24(doc)
    elif argv[2] == "HSMUN":
        doc = HSMUN23(doc)
    else:
        print("nonvalid book thing")
        return
    
    for text in doc.output:
        print("{} {} {} ---------------------------- {}".format(
            text["country"], text["category"],
            text["legislation_title"], text["text"]
        ))

if __name__ == "__main__":
    import sys 

    main()