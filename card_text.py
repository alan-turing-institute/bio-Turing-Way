import yaml
from yaml import Loader, dump, load
from bs4 import BeautifulSoup
import requests

# Defining the strings for the markdown file 

panel_starter_text = """:::{panels}
:container: +full-width text-center
:column: col-lg-6 px-2 py-2
:card: \n"""


title_card_end_string = "\n ^^^ \n"
footnote_start_string = "+++ \n"
card_ending_string = "\n --- \n"

panel_ending_string = "\n::: \n"

# Load the YAML file with the profiles and TOC whitelists
with open("mynewbook/profiles.yml") as f:
        profiles = load(f, Loader=Loader)

full_card_string = panel_starter_text

for profile_name, toc in profiles.items():
    
    toc_string = ""
    for chapter in toc:
        toc_string = toc_string + "- " + str(chapter) + "\n"

    full_card_string = full_card_string + str(profile_name) + toc_string + title_card_end_string + str(toc) + card_ending_string


    # Load the HTML file from each edition
    profile_directory = str(profile_name)
    with open("mynewbook_DSG/_build/html/search.html") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        toc_html_text = soup.find_all("a",class_="reference internal")
        
        chapters_string = ""
        for chapter_html in toc_html_text:
            chapter_ref_file = str(chapter_html.get('href'))
            chapter_title = str(chapter_html.get_text())
            chapter_title = chapter_title.strip()
            
            chapters_string = chapters_string + "- " + chapter_title + "\n" 

        print(chapters_string)

#Remove the last --- from the string otherwise a blank card is produced. 
full_card_string = full_card_string[:-len(card_ending_string)] 


full_card_string = full_card_string + panel_ending_string
#print(full_card_string)



