import yaml
from yaml import Loader, dump, load



# Loading the yaml file. 
def load_toc_file(toc_file_path):
    with open(toc_file_path) as t:
        toc_dictionary = load(t, Loader=Loader)
        loop_dictionary(toc_dictionary)
    return toc_dictionary

# Loop through the yaml file to get the filenames from throughout the tree
def loop_dictionary(toc_dictionary):
    if type(toc_dictionary) == dict:
        for item in toc_dictionary.items():
            get_file_strings(item)
    else:
        raise Exception('Not a dictionary')

# Create a list of strings of the filenames within the TOC
def get_file_strings(item):
    if item[0] == 'file':
        return filelist.append(item[1])
    elif item[0] in ['parts','chapters','sections']:
        for entry in item[1]:
            loop_dictionary(entry)
            
# Get titles from markdown files
def get_title(filelist):
    title_list = []

    for filedir in filelist:
        with open(filedir) as t:
            print(t[0])
    return title_list

# Create the button for the link to the edition
def create_edition_button(edition_title):

    edition_url = "https://the-turing-way-choose-your-own-adventure.netlify.app/pathway/"
    button_url = edition_url + edition_title
    
    button_start = "```{link-button} " + button_url + "\n"
    button_text = ":text: " + edition_title + "\n"
    button_option = ":classes: bg-info text-white text-center font-weight-bold \n"
    button_end = "```"
    edition_button = button_start + button_text + button_option + button_end
    return edition_button

# Loop through each item of the table of contents to create bullet points
def create_toc_bullets(filename_list):
    toc_string = "\n"

    for filename in filename_list:
        filename = "[](" + filename + ")"
        toc_string = toc_string + "- " + filename + "\n"

    return toc_string

# Creating bullet points with hyperlinks to the different pages
def create_card_with_toc(edition_title,filename_list):
    
    title_end_string = "\n ^^^ "
    card_ending_string = "\n --- \n"
    
    edition_button = create_edition_button(edition_title)

    toc_string = create_toc_bullets(filename_list)
    card_string = edition_button + title_end_string + toc_string + card_ending_string
    return card_string

def create_panels(edition_title,filename_list):
    panel_start = """:::{panels}
    :container: +full-width text-center
    :column: col-lg-6 px-2 py-2
    :card: \n"""

    card_string = create_card_with_toc(edition_title,filename_list)

    panel_end = "\n::: \n"

    panel_string = panel_start + card_string + panel_end 
    return panel_string

filelist = []
titlelist = []
toc_file_path = 'dsg/_toc.yml'
edition_title = 'dsg'

toc_dictionary = load_toc_file(toc_file_path)

panel_string = create_panels(edition_title, filelist)   


print('\n')
print(titlelist)
print('\n')
