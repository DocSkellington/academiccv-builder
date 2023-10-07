from pathlib import Path
from shutil import copytree

from cvbuilder import Builder
from cvbuilder.contexts.latex import LaTeXContext, Style
from cvbuilder.contexts.html import HTMLContext
from cvbuilder.contexts.markdown import MarkdownContext
from cvbuilder.modules.text import TextModule, LinkModule
from cvbuilder.modules.job import JobModule
from cvbuilder.modules.talk import TalkModule
from cvbuilder.modules.teach import TeachModule
from cvbuilder.modules.publication import PublicationModule
from cvbuilder.modules.supervision import SupervisionModule
from cvbuilder.modules.project import ProjectModule
from cvbuilder.modules.summary import SummaryModule
from cvbuilder.modules.logos import LogosModule
from cvbuilder.modules.event import EventModule
from cvbuilder.modules.award import AwardModule
from cvbuilder.modules.language import LanguageModule
from cvbuilder.modules.contact import ContactModule

# Copy resources folder
copytree("resources/", "output/html/resources/", dirs_exist_ok=True)

# HTML (producing two different files)
builder = Builder()

html = HTMLContext("output/html/index.html")
html.add_css_file("resources/css/style.css")
html.add_css_file("resources/css/sidebar.css")
html.add_css_file("resources/css/summary.css")

builder.add_context(html)

builder.add_module("contact", ContactModule(), "sidebar")
builder.add_module("languages", LanguageModule(), "sidebar")

builder.add_module("logos", LogosModule())
builder.add_module("summary", SummaryModule())
builder.add_module("jobs", JobModule())
builder.add_module(
    None,
    LinkModule(
        section="Publications",
        before="Consult the ",
        link="publications.html",
        text="Publications",
        after=" page.",
        icon="iconoir-journal"
    ),
)
builder.add_module("talks", TalkModule())
builder.add_module("teaching", TeachModule())
builder.add_module("supervision", SupervisionModule())
builder.add_module("projects", ProjectModule())
builder.add_module("events", EventModule())
builder.add_module("awards", AwardModule())
builder.add_module(
    None,
    TextModule(
        section="Closing Words",
        text="Doctor, I let you go.",
    ),
)

builder.build("example.json")

builder = Builder()

html = HTMLContext("output/html/publications.html")
html.set_title_fct(lambda personal: f"{personal.name} - Publications")

html.add_css_file("resources/css/style.css")
html.add_css_file("resources/css/sidebar.css")

builder.add_context(html)

builder.add_module("publications", PublicationModule())

builder.build("example.json")

# Example for LaTeX
builder = Builder()
latex = LaTeXContext("output/latex/example.tex")
latex.set_style("title", Style({"author": "\\bfseries"}))

builder.add_context(latex)

builder.add_module("contact", ContactModule(), "title")
builder.add_module("jobs", JobModule())
builder.add_module("publications", PublicationModule())
builder.add_module("talks", TalkModule())
builder.add_module("teaching", TeachModule())
builder.add_module("supervision", SupervisionModule())
builder.add_module("projects", ProjectModule())

builder.build(Path("example.json"))

# Example for Markdown
builder = Builder()
markdown = MarkdownContext("output/markdown/index.md", "Academic CV")

builder.add_context(markdown)

builder.add_module("logos", LogosModule())
builder.add_module("summary", SummaryModule())
builder.add_module("jobs", JobModule())
builder.add_module("projects", ProjectModule())
builder.add_module("awards", AwardModule())
builder.add_module("publications", PublicationModule())
builder.add_module("talks", TalkModule())
builder.add_module(
    None,
    LinkModule(
        section="Events",
        before="Consult the ",
        link="events.md",
        text="Events",
        after=" page.",
    ),
)
builder.add_module("teaching", TeachModule())
builder.add_module("supervision", SupervisionModule())

builder.build(Path("example.json"))
