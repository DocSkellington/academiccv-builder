from pathlib import Path
from shutil import copytree

from cvbuilder.builder import Builder
from cvbuilder.contexts import Style
from cvbuilder.contexts.latex import LaTeXContext
from cvbuilder.contexts.html import HTMLContext
from cvbuilder.modules.text import TextModule, LinkModule
from cvbuilder.modules.job import JobModule
from cvbuilder.modules.publication import PublicationModule


if __name__ == "__main__":
    # Copy resources folder
    copytree("resources/", "output/html/resources/", dirs_exist_ok=True)

    # HTML (producing two different files)
    builder = Builder()

    html = HTMLContext("output/html/index.html")
    html.add_css_file("resources/css/main.css")
    html.add_css_file("resources/css/sidebar.css")
    html.add_css_file("resources/css/item.css")

    builder.add_context(html)

    builder.add_module(
        None,
        TextModule(
            section="Summary",
            text="Do you know what I am? I am an idiot! With a blue box and a screwdriver!",
        ),
    )
    builder.add_module("work", JobModule())
    builder.add_module(
        None,
        LinkModule(
            section="Publications",
            before="Consult the ",
            link="publications.html",
            text="Publications",
            after=" page.",
        ),
    )

    builder.build("example.json")

    builder = Builder()

    html = HTMLContext("output/html/publications.html")
    html.set_title_fct(lambda personal: f"{personal.name} - Publications")

    html.add_css_file("resources/css/main.css")
    html.add_css_file("resources/css/sidebar.css")
    html.add_css_file("resources/css/item.css")

    builder.add_context(html)

    builder.add_module("publications", PublicationModule())

    builder.build("example.json")

    # Example for LaTeX
    # TODO: add Markdown context
    builder = Builder()
    latex = LaTeXContext("output/latex/example.tex")
    latex.set_style("title", Style({"author": "\\bfseries"}))

    builder.add_context(latex)

    builder.add_module("work", JobModule())
    builder.add_module("publications", PublicationModule())

    builder.build(Path("example.json"))
