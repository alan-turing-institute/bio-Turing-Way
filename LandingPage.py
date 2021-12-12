from main import get_toc_and_profiles
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import mdutils as mdutils
import os

class CuratedPage:
  def __init__(self, page_path, page_title, page_parent):
    self.page_path=page_path
    self.page_title=page_title
    self.page_parent = page_parent

  def __str__(self):
    aboutme = "Path: {0}\nTitle: {1} Parent:{2}".format(self.page_path, self.page_title,self.page_parent)
    return aboutme

class LandingPage:
  book_path = ''
  def __init__(self, persona=""):
    self.persona = persona
    self.curated_pages = []
    self.landing_page_title = "Landing Page:"

  def __str__(self):
    aboutme = "Persona: {0}\n Title: {1}\n".format(self.persona, self.landing_page_title)
    for p in range(0,len(self.curated_pages)):
      aboutme = aboutme + "{0}\n".format(self.curated_pages[p])
    return aboutme
  
  def set_class_variable(self, book_path):
    self.book_path = book_path

  def gather_curated_page_paths(self, toc):
    book = toc['parts'][0]
    chapters = book['chapters']
    parent = 1
    curated_pages = []
    def getAllFiles(parent, listOfSectionsOrFiles, curated_pages):
      for section in listOfSectionsOrFiles:
        if 'file' in section:
          new_page = {'parent': parent, 'file_path': section['file']+".md"}
          curated_pages.append(new_page)
        if 'sections' in section:
          getAllFiles(parent+1,section['sections'], curated_pages)
      return curated_pages    

    curated_pages = getAllFiles(parent, chapters, curated_pages)
    return curated_pages

  
  def populate_from_curated_pages(self, curated_pages:list):
    """Get curated page titles to be used in generating toc"""
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

    for curated_page in curated_pages:
      curated_page_path=os.path.join(self.book_path,curated_page['file_path'])
      curated_page_parent = curated_page['parent']
      with open(curated_page_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        md = (MarkdownIt())
        tokens:list = md.parse(text)
        
        header_opens = list_header_open(tokens)
        header_ones = list_header_one(header_opens)
        header_content_index = tokens.index(header_ones[0])+1
        header_content = tokens[header_content_index].content
        a_curated_page = CuratedPage(page_path=curated_page['file_path'], 
          page_title=header_content,
          page_parent=curated_page_parent)
        self.curated_pages.append(a_curated_page)
    return self

  def writeContent(self):
    """Populate landing page with curated toc"""
    new_landing_page_path = os.path.join(self.book_path,self.persona)
    mdFile = mdutils.MdUtils(file_name=new_landing_page_path)
    # mdFile.new_header(level=1, title=self.landing_page_title, add_table_of_contents='n')
    intro_paragraph = "These are the pages curated for {0}".format(self.persona.upper())
    mdFile.new_paragraph(intro_paragraph)
    
    for curated_page in self.curated_pages:
      curated_page:CuratedPage = curated_page
      list_indent:str = ''
      for s in range(0, (curated_page.page_parent-1)*4):
        list_indent:str = list_indent.__add__(" ")
      list_indent = list_indent.__add__("- ")
      link = os.path.join('./',curated_page.page_path)
      md_link=mdFile.new_inline_link(link=link, text=curated_page.page_title)
      mdFile.new_line(list_indent+md_link)
      # mdFile.new_line(mdFile.new_inline_link(link=link, text=curated_page.page_title))
    
    mdFile.create_md_file()

def sketchMe(curate_page_paths):
  aLandingPage=LandingPage("test")
  aLandingPage = aLandingPage.populate_curated_pages(curate_page_paths)
  print(aLandingPage)

if __name__ == "__main__":
  curate_page_paths = ['/Users/myong/Documents/workspace/bio-Turing-Way/mynewbook/intro.md']
  sketchMe(curate_page_paths)  # pragma: no cover



# with open(book_path, "r", encoding="utf-8") as input_file:
#     text = input_file.read()
# md = (
#     MarkdownIt()
# )
# tokens = md.parse(text)
# print(type(tokens))
# print(tokens[1].content)