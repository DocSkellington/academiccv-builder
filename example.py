import shutil

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
shutil.copytree("resources/", "output/html/resources/", dirs_exist_ok=True)

builder = Builder()

# Main page of HTML
main_html = HTMLContext("output/html/index.html")
builder.add_context(main_html)

main_html.add_css_file("resources/css/style.css")
main_html.add_css_file("resources/css/sidebar.css")
main_html.add_css_file("resources/css/summary.css")

main_html.add_module("contact", ContactModule(), "sidebar")
main_html.add_module("languages", LanguageModule(), "sidebar")
main_html.add_module("logos", LogosModule())
main_html.add_module("summary", SummaryModule())
main_html.add_module("jobs", JobModule())
main_html.add_module(
    None,
    LinkModule(
        section="Publications",
        before="Consult the ",
        link="publications.html",
        text="Publications",
        after=" page.",
        icon="iconoir-journal",
    ),
)
main_html.add_module("talks", TalkModule())
main_html.add_module("teaching", TeachModule())
main_html.add_module("supervision", SupervisionModule())
main_html.add_module("projects", ProjectModule())
main_html.add_module("events", EventModule())
main_html.add_module("awards", AwardModule())
main_html.add_module(
    None,
    TextModule(
        section="Closing Words",
        text="Doctor, I let you go.",
    ),
)

# HTML publications page
publication_html = HTMLContext("output/html/publications.html")
builder.add_context(publication_html)

publication_html.set_title_fct(lambda personal: f"{personal.name} - Publications")
publication_html.add_css_file("resources/css/style.css")
publication_html.add_css_file("resources/css/sidebar.css")

publication_html.add_module("publications", PublicationModule())

# LaTeX output
latex = LaTeXContext("output/latex/example.tex")
builder.add_context(latex)

latex.set_style("title", Style({"author": "\\bfseries"}))

latex.add_module("contact", ContactModule(), "title")
latex.add_module("jobs", JobModule())
latex.add_module("publications", PublicationModule())
latex.add_module("talks", TalkModule())
latex.add_module("teaching", TeachModule())
latex.add_module("supervision", SupervisionModule())
latex.add_module("projects", ProjectModule())

# Markdown
markdown = MarkdownContext("output/markdown/index.md", "Academic CV")
builder.add_context(markdown)

markdown.add_module("logos", LogosModule())
markdown.add_module("summary", SummaryModule())
markdown.add_module("jobs", JobModule())
markdown.add_module("projects", ProjectModule())
markdown.add_module("awards", AwardModule())
markdown.add_module("publications", PublicationModule())
markdown.add_module("talks", TalkModule())
markdown.add_module(
    None,
    LinkModule(
        section="Events",
        before="Consult the ",
        link="events.md",
        text="Events",
        after=" page.",
    ),
)
markdown.add_module("teaching", TeachModule())
markdown.add_module("supervision", SupervisionModule())

# Build every context from the file
builder.build(
    [
        "json_example/example.json",
        "json_example/summary.json",
        "json_example/publications.json",
    ]
)
