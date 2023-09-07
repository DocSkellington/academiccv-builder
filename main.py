from pathlib import Path

from cvbuilder.builder import Builder
from cvbuilder.contexts.latex import LaTeXContext, Style
from cvbuilder.modules.job import JobModule
from cvbuilder.modules.publication import PublicationModule


if __name__ == "__main__":
    builder = Builder()

    latex = LaTeXContext(Path("output/example.tex"))
    latex.set_style("title", Style({"author": "\\bfseries"}))

    builder.add_context(latex)

    builder.add_module("work", JobModule())
    builder.add_module("publications", PublicationModule())

    builder.build(Path("example.json"))
