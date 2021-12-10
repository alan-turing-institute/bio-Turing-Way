import yaml
from yaml import Loader, dump, load


heading_title = "## Different Profiles"
filelist = []


# Main function: Read in TOC list and markdown path
def edit_welcome_md(path_welcome_md, toc_dict_list, profiles_list):

    # Create a list of all the filenames from every toc
    list_filelist = loop_dictionary_list(toc_dict_list)

    # Create a list of all the md titles from every toc
    list_titlelist = get_titles_from_filenames(list_filelist)

    # ToDo Add some debugging print statements (or get the VSCode debugger to work)
    
    # Create panel string using the toc titles
    panel_string = create_panel(list_titlelist, list_filelist, profiles_list)

    # Insert panel into the welcome md file
    insert_into_md(path_welcome_md, heading_title, panel_string)


# Take the markdown file, add the panels, and save the markdown file.
def insert_into_md(path_welcome_md, heading_title, panel_string):

    md_text = get_text_from_md(path_welcome_md)
    new_md_text = insert_text_after_string(md_text, heading_title, panel_string)
    overwrite_md(new_md_text, path_welcome_md)


# Get the text from the markdown file
def get_text_from_md(path_welcome_md):
    with open(path_welcome_md, "r") as md:
        md_text = md.readlines()
    return md_text


# Look for a heading and insert string after that heading
def insert_text_after_string(md_text, heading_title, panel_string):
    new_md_text = ""
    for line in md_text:
        if line.startswith(heading_title):
            new_md_text += line + panel_string
        else:
            new_md_text += line
    return new_md_text


# Overwrite the markdown file with new added panel text.
def overwrite_md(new_md_text, path_welcome_md):
    with open(path_welcome_md, "w") as txt:
        txt.write(new_md_text)


# Grab the top-most heading from a markdown file
def get_heading(md_text, heading_string="# "):
    md_title_string = ""
    for line in md_text:
        if line.startswith(heading_string):
            md_title_string += line
            break
    md_title = md_title_string.replace(heading_string, "")
    return md_title


# Loop through the dictionary TOC and get the filename from throughout the tree
def loop_dictionary(toc_dictionary):
    for item in toc_dictionary.items():
        get_file_strings(item)


# Create a list of strings of the filenames within the TOC
def get_file_strings(item):
    if item[0] == "file":
        filelist.append(item[1])
        return filelist
    elif item[0] in ["parts", "chapters", "sections"]:
        for entry in item[1]:
            loop_dictionary(entry)


# Grab an example TOC dictionary
def load_toc_file(toc_file_path):
    with open(toc_file_path) as t:
        toc_dictionary = load(t, Loader=Loader)
        loop_dictionary(toc_dictionary)
    return toc_dictionary


# Loop through the list of TOC dictionaries
def loop_dictionary_list(toc_dict_list):
    number_of_tocs = len(toc_dict_list)
    list_filelist = [[] for i in range(number_of_tocs)]

    for counter, toc_dict in enumerate(toc_dict_list):
        # Make sure the filelist is clear
        if filelist:
            filelist.clear()
        # Loop through the given TOC and keep the filenames
        loop_dictionary(toc_dict)
        # Add the filenames to a list of lists
        list_filelist[counter] = filelist
    return list_filelist


# For each item in each TOC, get the heading name from the md file
def get_titles_from_filenames(list_filelist):
    number_of_tocs = len(list_filelist)
    list_titlelist = [[] for i in range(number_of_tocs)]
    titlelist = []
    for counter, list_files in enumerate(list_filelist):

        # Make sure the title list is clear
        if titlelist:
            titlelist.clear()

        # Loop through the files and get the headings
        for file in list_files:
            filepath = "master/" + file + ".md"
            md_text = get_text_from_md(filepath)
            md_title = get_heading(md_text, heading_string="# ")
            titlelist.append(md_title.strip())

        list_titlelist[counter] = titlelist
    return list_titlelist


# From the list of titles for a single toc, create a bullet point string.
def create_bullet_string(titlelist,file_list):
    toc_string = ""
    for counter, title in enumerate(titlelist):
        if counter >= 3:
            toc_string = toc_string + "- And more! \n"
            break
        # If we create "editions", these may need to be <a href=''> type links
        toc_string = toc_string + "- [" + title +"](" + file_list[counter] + ")\n"
    return toc_string


# Create panel
def create_panel(list_titlelist, list_filelist, profile_list):
    number_of_tocs = len(list_titlelist)

    panel_start = """\n:::{panels}
:container: +full-width 
:column: col-lg-6 px-2 py-2
:header: text-center bg-white
:card: text-left shadow
:footer: text-left\n"""

    panel_string = panel_start
    panel_end = "\n::: \n"

    for counter, toc_list in enumerate(list_titlelist):

        button_string = create_profile_button(profile_list[counter])
        file_list = list_filelist[counter]
        toc_string = create_bullet_string(toc_list,file_list)
        panel_string = panel_string + button_string + toc_string
        if counter != number_of_tocs - 1:
            panel_string = panel_string + "\n---\n"
    panel_string = panel_string + panel_end
    return panel_string


# Create the button linking to the profile
def create_profile_button(profile_name):
    # ToDo Change this to either a relative path or, at least, the real Turing Way URL
    profile_url = "https://the-turing-way-choose-your-own-adventure.netlify.app/editions/"
    start_button = "\n```{link-button} "
    text_button = "\n:text: "
    option_button = """\n:classes: bg-info text-white text-center font-weight-bold
```"""
    end_card_header = "\n^^^\n"

    button_string = start_button + profile_url + profile_name
    button_string = button_string + text_button + profile_name
    button_string = button_string + option_button + end_card_header
    return button_string


def add_cards(profile_list, toc_dict_list, welcome_path):
    """Takes a list of profile names and a list of tocs. Creates and inserts cards."""

    edit_welcome_md(welcome_path, toc_dict_list, profile_list)


# # Testing area
path_welcome_md = "master_enrichment/welcomeTest.md"

example_toc =  load_toc_file('master_dsg/_toc.yml')
another_toc = load_toc_file('master_enrichment/_toc.yml')
third_toc = load_toc_file('master_group-leader/_toc.yml')
toc_dict_list = [example_toc,another_toc,third_toc]

profiles_list = ["dsg","enrichment","group-leader"]

edit_welcome_md(path_welcome_md, toc_dict_list, profiles_list)


# Broken things:
# - Don't have the button titles DONE
# - Don't have the button links DONE
# - Don't have the toc links
# - Limit the number of bullet points DONE
