"""Create landing pages for each profile."""
import os

import mdutils
from markdown_it import MarkdownIt


class LandingPage:
    """This class generates a markdown page.
    Input:
    1. Path of Jupyter book,
    2. Label for audience of markdown page (eg. dsg)
    3. A list containing the toc files whitelisted for this audience
    Output:
    1. A markdown page containing a toc with links curated for this audience
    """

    # This is the path of the jupyter book
    book_path = ""

    def __init__(self, persona="", landing_name=""):
        # This is the audience label
        self.persona = persona
        #  This is the title of the landing page
        self.landing_page_title = "Table of Contents for: {0}".format(self.persona)
        #  This is the path of the landing page
        # self.landing_page_path = os.path.join(self.book_path, self.persona)
        self.landing_page_path = os.path.join(self.book_path, landing_name)
        # This is the instance of the class used to generate a markdown file.
        # It is instantiated with the name of the file.
        self.md_file = mdutils.MdUtils(file_name=self.landing_page_path)
        self.curated_links = []

    def __str__(self):
        aboutme = "Persona: {0}\n Title: {1}\n".format(
            self.persona, self.landing_page_title
        )
        return aboutme

    def gather_curated_links(self, toc):
        """This generates a list containing markdown links to whitelisted pages
        Input: Whitelisted toc (files and sections), arranged as required by
               the layout of the toc
        Output: Links with url and page title, arranged as required by the
                layout of the toc
        """

        def get_links_of_section(list_of_sections_or_file):
            curated_links = []
            for section in list_of_sections_or_file:
                if "file" in section:
                    # Create a link to whitelisted file
                    link = os.path.join("./", section["file"] + ".md")
                    # title = self.get_title_from_curated_page(link)
                    md_link = self.md_file.new_inline_link(link=link, text="")
                    curated_links.append(md_link)
                if "sections" in section:
                    curated_links.append(get_links_of_section(section["sections"]))
            return curated_links

        book = toc["parts"][0]
        chapters = book["chapters"]
        self.curated_links = get_links_of_section(chapters)

    def get_title_from_text(self, markdown_text):
        def list_header_open(tokens: list) -> list:
            header_opens = []
            for t in tokens:
                if t.type == "heading_open":
                    header_opens.append(t)
            return header_opens

        def list_header_one(header_opens: list):
            header_ones = []
            for t in header_opens:
                if t.tag == "h1":
                    header_ones.append(t)
            return header_ones

        md = MarkdownIt()
        tokens: list = md.parse(markdown_text)
        header_opens = list_header_open(tokens)
        header_ones = list_header_one(header_opens)
        header_content_index = tokens.index(header_ones[0]) + 1
        header_content = tokens[header_content_index].content
        return header_content

    def get_title_from_curated_page(self, curated_page_path):
        """Get title from curated page, given path"""

        header_content = "Page:{0} title is not found".format(curated_page_path)
        curated_page_path = os.path.join(self.book_path, curated_page_path)
        with open(curated_page_path, "r", encoding="utf-8") as input_file:
            markdown_text = input_file.read()
            header_content = self.get_title_from_text(markdown_text)
        return header_content

    def write_content(self):
        """Populate landing page with curated toc"""
        self.md_file.new_header(
            level=1, title=self.landing_page_title, add_table_of_contents="n"
        )
        intro_paragraph = "These are the pages curated for {0}".format(
            self.persona.upper()
        )
        self.md_file.new_paragraph(intro_paragraph)
        self.md_file.new_list(self.curated_links)
        self.md_file.create_md_file()
        print(self.md_file.file_data_text)
        return self.md_file.file_data_text
