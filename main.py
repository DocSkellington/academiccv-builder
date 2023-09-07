from pathlib import Path

from cvbuilder.builder import Builder
from cvbuilder.contexts.latex import LaTeXContext
from cvbuilder.modules.job import JobModule
from cvbuilder.modules.publication import PublicationModule


if __name__ == "__main__":
    builder = Builder()

    builder.add_context(LaTeXContext(Path("output/example.tex")))

    builder.add_module("work", JobModule())
    builder.add_module("publications", PublicationModule())

    builder.build(Path("example.json"))
