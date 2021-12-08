from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import mdutils as mdutils

class LandingPage:
  def __init__(self, persona=""):
    self.persona = persona
    self.curated_page_titles = []
    self.landing_page_title = "Landing Page:"

  def __str__(self):
    aboutme = "Persona: {0}\n Path: {1}\n Title: {2}".format(self.persona, self.curated_page_titles, self.landing_page_title)
    return aboutme
  
  def getPageTitles(self, curated_page_paths:list):
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

    for page_path in curated_page_paths:
      with open(page_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        md = (MarkdownIt())
        tokens:list = md.parse(text)
        
        header_opens = list_header_open(tokens)
        header_ones = list_header_one(header_opens)
        header_content_index = tokens.index(header_ones[0])+1
        header_content = tokens[header_content_index].content
        self.curated_page_titles.append(header_content)
    return self

  def setPageContent(self):
    mdFile = mdutils.MdUtils(file_name='./mynewbook/Example_Markdown')
    mdFile.new_header(level=1, title=self.landing_page_title, add_table_of_contents='n')
    intro_paragraph = "These are the pages curated for {0}".format(self.persona.upper())
    mdFile.new_paragraph(intro_paragraph)
    
    for title in self.curated_page_titles:
      mdFile.new_header(level=1, title=title)

    mdFile.new_table_of_contents(table_title='Curated Pages for {0}'.format(self.persona), depth=2)
    mdFile.create_md_file()

def sketchMe():
  curate_page_paths = ['/Users/myong/Documents/workspace/bio-Turing-Way/mynewbook/intro.md']
  aLandingPage=LandingPage("test")
  aLandingPage = aLandingPage.getPageTitles(curate_page_paths)
  aLandingPage.setPageContent()
  print(aLandingPage)

def getLandingPage(book_path, profiles_and_tocs):
  print(book_path)
  for p in range(0,len(profiles_and_tocs)):
    profile = profiles_and_tocs[p][0]
    toc = profiles_and_tocs[p][1]
    print(profile)
    print(toc['parts'])


if __name__ == "__main__":
  sketchMe()  # pragma: no cover



# with open(book_path, "r", encoding="utf-8") as input_file:
#     text = input_file.read()
# md = (
#     MarkdownIt()
# )
# tokens = md.parse(text)
# print(type(tokens))
# print(tokens[1].content)