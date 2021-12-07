from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

class LandingPage:
  def __init__(self, persona="", page_path=""):
    self.persona = persona
    self.page_path = page_path
    self.page_title = "This is a test title"
  
  def __str__(self):
    aboutme = "Persona: {0}\n Path: {1}\n Title: {2}".format(self.persona, self.page_path, self.page_title)
    return aboutme
  
  def setPageTitle(self):
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

    with open(self.page_path, "r", encoding="utf-8") as input_file:
      text = input_file.read()
      md = (MarkdownIt())
      tokens:list = md.parse(text)
      # for t in range(0, len(tokens)):
      #   print("Index: {0}, Type: {1}\n".format(t, tokens[t]))
      
      header_opens = list_header_open(tokens)
      header_ones = list_header_one(header_opens)
      header_content_index = tokens.index(header_ones[0])+1
      header_content = tokens[header_content_index].content
      self.page_title = header_content
      return self

page_path = '/Users/myong/Documents/workspace/bio-Turing-Way/mynewbook/intro.md'    
aLandingPage=LandingPage("test",page_path)

aLandingPage = aLandingPage.setPageTitle()
print(aLandingPage)

anotherLandingPage = LandingPage()
print(anotherLandingPage)


# with open(book_path, "r", encoding="utf-8") as input_file:
#     text = input_file.read()
# md = (
#     MarkdownIt()
# )
# tokens = md.parse(text)
# print(type(tokens))
# print(tokens[1].content)