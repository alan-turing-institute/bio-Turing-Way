import yaml
from yaml import Loader, dump, load

path_welcome_md = "master/welcomeTest.md"
panel_string = "\nTEST TEST TEST \n"
heading_title = "## Different Profiles"
toc_dict_list = []
filelist = []


# Main function: Read in TOC list and markdown path
def edit_welcome_md(path_welcome_md,toc_dict_list):


    # Create cards
    
    

    # Create panel 



    # Edit the markdown file
    insert_into_md(path_welcome_md,heading_title,panel_string)


# Take the markdown file, add the panels, and save the markdown file. 
def insert_into_md(path_welcome_md,heading_title,panel_string):

    md_text = get_text_from_md(path_welcome_md)
    new_md_text = insert_text_after_string(md_text,heading_title, panel_string) 
    overwrite_md(new_md_text,path_welcome_md)
   
# Get the text from the markdown file
def get_text_from_md(path_welcome_md):
    with open(path_welcome_md, 'r') as md:
        md_text = md.readlines()
    return(md_text)

# Look for a heading and insert string after that heading
def insert_text_after_string(md_text,heading_title, panel_string):
    new_md_text = ""
    for line in md_text:
        if line.startswith(heading_title):
            new_md_text += line + panel_string
        else:
            new_md_text += line
    return(new_md_text)

# Overwrite the markdown file with new added panel text. 
def overwrite_md(new_md_text,path_welcome_md):
     with open(path_welcome_md, 'w') as txt:
        txt.write(new_md_text)

# Grab the top-most heading from a markdown file
def get_heading(md_text, heading_string = "# "):
    md_title_string = ""
    for line in md_text:
        if line.startswith(heading_string):
            md_title_string += line
            break
    md_title = md_title_string.replace(heading_string,"")
    return(md_title)

# Loop through the dictionary TOC and get the filename from throughout the tree
def loop_dictionary(toc_dictionary):
    for item in toc_dictionary.items():
            get_file_strings(item)

# Create a list of strings of the filenames within the TOC
def get_file_strings(item):
    if item[0] == 'file':
        return filelist.append(item[1])
    elif item[0] in ['parts','chapters','sections']:
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
    for toc_dict in toc_dict_list:
        # Make sure the filelist is clear for each new TOC
        if filelist:
            filelist.clear()
        loop_dictionary(toc_dict)

# # Testing area

example_toc =  load_toc_file('dsg/_toc.yml')
toc_dict_list = [example_toc,example_toc,example_toc]

md_text = get_text_from_md(path_welcome_md)
md_title = get_heading(md_text, heading_string = "# ")


print('\n')
print(md_title)
print('\n')