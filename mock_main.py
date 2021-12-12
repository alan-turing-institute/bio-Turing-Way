import main as services
import LandingPage as LandingPageClass
from yaml import Loader, dump, load
import os


def setPageContent(book_path, profiles_and_tocs):
  """Get the each persona and generate a landing page"""
  LandingPageClass.LandingPage.book_path=book_path
  for p in range(0,len(profiles_and_tocs)):
    profile = profiles_and_tocs[p][0]
    white_listed_toc = profiles_and_tocs[p][1]
    aLandingPage = LandingPageClass.LandingPage(persona=profile)
    # print (white_listed_toc)
    curated_links = aLandingPage.gather_curated_links(white_listed_toc)
    # curated_page_paths = aLandingPage.gather_curated_page_paths(white_listed_toc)
    # aLandingPage.populate_from_curated_pages(curated_page_paths)
    aLandingPage.writeContent(curated_links)
    # print(aLandingPage)

if __name__ == "__main__":
  book_path = os.path.join(os.path.dirname(__file__),'master')
  # print(book_path)
  toc, profiles = services.get_toc_and_profiles(book_path=book_path)
  profiles_and_tocs = list(services.generate_tocs(toc, profiles))
  setPageContent(book_path,profiles_and_tocs)
