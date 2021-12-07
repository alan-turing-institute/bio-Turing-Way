import main as services
import LandingPage as landingPage
from yaml import Loader, dump, load


book_path = '/Users/myong/Documents/workspace/bio-Turing-Way/mynewbook'
toc, profiles = services.get_toc_and_profiles(book_path=book_path)
# print(profiles)
# print(toc)

md = (
    MarkdownIt()
)
text = ("""# Welcome to your Jupyter Book

This is a small sample book to give you a feel for how book content is
structured.

:::{note}
Here is a note!
:::

And here is a code block:

```
e = mc^2
```

Check out the content pages bundled with this sample book to see more.
  """)

tokens = md.parse(text)
print(tokens[0])