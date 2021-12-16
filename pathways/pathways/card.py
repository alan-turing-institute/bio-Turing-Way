"""Create Cards for the Welcome page."""

HEADING_TITLE = "## Different Profiles"

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

def create_bullet_string(file_list):
    """From the list of files for a single toc, create a bullet point string."""
    toc_string = ""

    for f in file_list[0:3]:
        toc_string += "- [](" + f + ")\n"

    if len(file_list) > 3:
        toc_string += "\nAnd more... \n"

    return toc_string

def create_card(profile_name, file_list, landing_name):
    """Create a single card."""
    button_string = create_profile_button(profile_name, landing_name)
    toc_string = create_bullet_string(file_list)
    return button_string + toc_string

def create_panel(list_cards):
    """Create the full panel, with all cards.""" 

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

def create_profile_button(profile_name, landing_name):
    """Create the button linking to the profile."""
    # relative_path = "./" + profile_name.lower() + ".html"
    relative_path = "./{0}.html".format(landing_name)
    start_button = "```{link-button} "
    text_button = "\n:text: "
    option_button = "\n:classes: bg-info text-white text-center font-weight-bold\n```"
    end_card_header = "\n^^^\n"

    button_string = start_button + relative_path
    button_string += text_button + profile_name
    button_string += option_button + end_card_header
    return button_string
