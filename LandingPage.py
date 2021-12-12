
import main as services
from markdown_it import MarkdownIt
import mdutils as mdutils
import os

class LandingPage:
  book_path = ''
  def __init__(self, persona=""):
    self.persona = persona
    self.curated_pages = []
    self.landing_page_title = "Table of Contents for: {0}".format(self.persona)
    self.landing_page_path = os.path.join(self.book_path,self.persona)
    self.mdFile = mdutils.MdUtils(file_name=self.landing_page_path)

  def __str__(self):
    aboutme = "Persona: {0}\n Title: {1}\n".format(self.persona, self.landing_page_title)
    for p in range(0,len(self.curated_pages)):
      aboutme = aboutme + "{0}\n".format(self.curated_pages[p])
    return aboutme
  
  def set_class_variable(self, book_path):
    self.book_path = book_path

  def gather_curated_links(self, toc):
    book = toc['parts'][0]
    chapters = book['chapters']
    curated_links = []

    def getLinksOfSection(listOfSectionsOrFiles):
      curated_links = []
      for section in listOfSectionsOrFiles:
        if 'file' in section:
          link = os.path.join('./',section['file']+".md")
          title = self.get_title_from_curated_page(link)
          md_link=self.mdFile.new_inline_link(link=link, text=title)
          curated_links.append(md_link)
          # print("Curated Files: {0}".format(curated_links))
        if 'sections' in section:
          # print("Sections: {0}".format(section['sections']))
          curated_links.append(getLinksOfSection(section['sections']))
      return curated_links

    curated_links= getLinksOfSection(chapters)
    return curated_links

  def get_title_from_curated_page(self, curated_page_path):
    def list_header_open(tokens:list)->list:
      header_opens = []
      for t in tokens:
        if (t.type=='heading_open'):
          header_opens.append(t)
      return header_opens
    
    def list_header_one(header_opens:list):
      header_ones = []
      for t in header_opens:
        if (t.tag=='h1'):
          header_ones.append(t)
      return header_ones
    
    header_content = "Page:{0} title is not found".format(curated_page_path)
    curated_page_path=os.path.join(self.book_path,curated_page_path)
    with open(curated_page_path, "r", encoding="utf-8") as input_file:
      text = input_file.read()
      md = (MarkdownIt())
      tokens:list = md.parse(text)
      header_opens = list_header_open(tokens)
      header_ones = list_header_one(header_opens)
      header_content_index = tokens.index(header_ones[0])+1
      header_content = tokens[header_content_index].content
    return header_content

  def writeContent(self, curated_links):
    """Populate landing page with curated toc"""
    self.mdFile.new_header(level=1, title=self.landing_page_title, add_table_of_contents='n')
    intro_paragraph = "These are the pages curated for {0}".format(self.persona.upper())
    self.mdFile.new_paragraph(intro_paragraph)
    self.mdFile.new_list(curated_links)   
    self.mdFile.create_md_file()

def setPageContent(book_path, profiles_and_tocs):
  """Get the each persona and generate a landing page"""
  LandingPage.book_path=book_path
  for p in range(0,len(profiles_and_tocs)):
    profile = profiles_and_tocs[p][0]
    white_listed_toc = profiles_and_tocs[p][1]
    aLandingPage = LandingPage(persona=profile)
    curated_links = aLandingPage.gather_curated_links(white_listed_toc)
    aLandingPage.writeContent(curated_links)

if __name__ == "__main__":
  book_path = os.path.join(os.path.dirname(__file__),'master')
  toc, profiles = services.get_toc_and_profiles(book_path=book_path)
  profiles_and_tocs = list(services.generate_tocs(toc, profiles))
  setPageContent(book_path,profiles_and_tocs)