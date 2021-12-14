"""Create Cards for the Welcome page."""

HEADING_TITLE = "## Different Profiles"
filelist = []


# Main function: Read in TOC list and markdown path
# def edit_welcome_md(path_welcome_md, toc_dict_list, profiles_list):

#     # Create a list of all the filenames from every toc
#     list_filelist = loop_dictionary_list(toc_dict_list)

#     # Create a list of all the md titles from every toc
#     list_titlelist = get_titles_from_filenames(list_filelist)

#     # ToDo Add some debugging print statements (or get the VSCode debugger to work)

#     # Create panel string using the toc titles
#     panel_string = create_panel(list_titlelist, list_filelist, profiles_list)

#     # Insert panel into the welcome md file
#     insert_into_md(path_welcome_md, heading_title, panel_string)


def insert_into_md(path_welcome_md, heading_title, panel_string):
    """Take the markdown file, add the panels, and save the markdown file."""

    md_text = get_text_from_md(path_welcome_md)
    new_md_text = insert_text_after_string(md_text, heading_title, panel_string)
    overwrite_md(new_md_text, path_welcome_md)


def get_text_from_md(path_welcome_md):
    """Get the text from the markdown file."""
    with open(path_welcome_md, "r", encoding="utf-8") as md:
        md_text = md.read()
    return md_text


def insert_text_after_string(md_text, heading_title, panel_string):
    """Look for a heading and insert string after that heading."""
    md_text = md_text.replace(heading_title, heading_title + "\n" + panel_string)
    return md_text


def overwrite_md(new_md_text, path_welcome_md):
    """Overwrite the markdown file with new added panel text."""
    with open(path_welcome_md, "w", encoding="utf-8") as txt:
        txt.write(new_md_text)


# Grab the top-most heading from a markdown file
# def get_heading(md_text, heading_string="# "):
#     md_title_string = ""
#     for line in md_text:
#         if line.startswith(heading_string):
#             md_title_string += line
#             break
#     md_title = md_title_string.replace(heading_string, "")
#     return md_title


# Loop through the dictionary TOC and get the filename from throughout the tree
# def loop_dictionary(toc_dictionary):
# for item in toc_dictionary.items():
#     get_file_strings(item)


# Create a list of strings of the filenames within the TOC
# def get_file_strings(item):
#     if item[0] == "file":
#         filelist.append(item[1])
#         return filelist
#     elif item[0] in ["parts", "chapters", "sections"]:
#         for entry in item[1]:
#             loop_dictionary(entry)


# # Grab an example TOC dictionary
# def load_toc_file(toc_file_path):
#     with open(toc_file_path) as t:
#         toc_dictionary = load(t, Loader=Loader)
#         loop_dictionary(toc_dictionary)
#     return toc_dictionary


# Loop through the list of TOC dictionaries
# def loop_dictionary_list(toc_dict_list):
#     number_of_tocs = len(toc_dict_list)
#     list_filelist = [[] for i in range(number_of_tocs)]

#     for counter, toc_dict in enumerate(toc_dict_list):
#         # Make sure the filelist is clear
#         if filelist:
#             filelist.clear()
#         # Loop through the given TOC and keep the filenames
#         loop_dictionary(toc_dict)
#         # Add the filenames to a list of lists
#         list_filelist[counter] = filelist
#     return list_filelist


# For each item in each TOC, get the heading name from the md file
# def get_titles_from_filenames(list_filelist):
#     number_of_tocs = len(list_filelist)
#     list_titlelist = [[] for i in range(number_of_tocs)]
#     for list_files in list_filelist:
#         list_titlelist.append(get_title_from_filename(list_files))
#     return list_titlelist


# def get_title_from_filename(file_list):
#     title_list = []
#     for f in file_list:
#         filepath = "master/" + f + ".md"
#         md_text = get_text_from_md(filepath)
#         md_title = get_heading(md_text, heading_string="# ")
#         title_list.append(md_title.strip())
#     return title_list


def create_bullet_string(file_list):
    """From the list of files for a single toc, create a bullet point string."""
    toc_string = ""

    for f in file_list[0:3]:
        toc_string += "- [](" + f + ")\n"

    if len(file_list) > 3:
        toc_string += "\nAnd more... \n"

    return toc_string


def create_card(profile_name, file_list):
    """Create a single card."""
    button_string = create_profile_button(profile_name)
    toc_string = create_bullet_string(file_list)
    return button_string + toc_string


def create_panel(list_cards):
    """Create the full panel, with all cards."""
    # number_of_tocs = len(list_titlelist)

    panel_start = (
        ":::{panels}\n"
        ":container: +full-width\n"
        ":column: col-lg-6 px-2 py-2\n"
        ":header: text-center bg-white\n"
        ":card: text-left shadow\n"
        ":footer: text-left\n"
    )

    panel_string = panel_start
    panel_end = "\n::: \n"
    panel_string += "\n---\n".join(list_cards)
    panel_string += panel_end
    return panel_string


def create_profile_button(profile_name):
    """Create the button linking to the profile."""
    relative_path = "./" + profile_name.lower() + ".html"
    start_button = "```{link-button} "
    text_button = "\n:text: "
    option_button = "\n:classes: bg-info text-white text-center font-weight-bold\n```"
    end_card_header = "\n^^^\n"

    button_string = start_button + relative_path
    button_string += text_button + profile_name
    button_string += option_button + end_card_header
    return button_string


# def add_cards(profile_list, toc_dict_list, welcome_path):
#     """Takes a list of profile names and a list of tocs. Creates and inserts cards."""

#     edit_welcome_md(welcome_path, toc_dict_list, profile_list)


################################################################

## Testing area for running these functions outside of main.py

# path_welcome_md = "master_copy/welcomeTest.md"

# Grabbing example toc files, in main.py these dictionaries are provided directly.
# example_toc =  load_toc_file('master_dsg/_toc.yml')
# another_toc = load_toc_file('master_enrichment/_toc.yml')
# third_toc = load_toc_file('master_group-leader/_toc.yml')
# toc_dict_list = [example_toc,another_toc,third_toc]

# Hard coded names, the main.py provides these directly.
# profiles_list = ["dsg","enrichment","group-leader"]

# edit_welcome_md(path_welcome_md, toc_dict_list, profiles_list)
