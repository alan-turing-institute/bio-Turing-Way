import main as services
import LandingPage as landingPage
from yaml import Loader, dump, load


book_path = '/Users/myong/Documents/workspace/bio-Turing-Way/master'
toc, profiles = services.get_toc_and_profiles(book_path=book_path)
profiles_and_tocs = list(services.generate_tocs(toc, profiles))
# print(profiles)
landingPage.getLandingPage(book_path, profiles_and_tocs)


